import os
import json

from datetime import datetime

import arxiv


def load_json(filename) -> dict | list:
    if filename and os.path.exists(filename):
        with open(filename, "rt") as f:
            return json.load(f)
    return []


def save_json(papers: list | dict, filename: str) -> None:
    with open(filename, "wt") as fh:
        json.dump(papers, fh, indent=2)


def load_known_papers(src_dir: str) -> set[str]:
    file = os.path.join(src_dir, "found_papers.json")
    return set(load_json(file))


def update_known_papers(old_papers: set[str], new_papers: list[dict]) -> None:
    old_papers.update(paper["paper_id"] for paper in new_papers)


def save_known_papers(papers: set[str], dst_dir: str) -> None:
    file = os.path.join(dst_dir, "found_papers.json")
    save_json(list(papers), file)


def fetch_new_papers_using_arxiv_client(query_terms: list[str], category: str, known_papers: set[str],
                                        max_results: int, page_size: int) -> \
        list[dict]:
    """Fetch new papers from arXiv using the Python client."""

    # Input validation
    page_size = min(page_size, max_results)

    # Construct the search query
    query_terms_all = []
    if query_terms:
        for term in [f'abs:"{term}"' for term in query_terms]:
            query_terms_all.append(term)
    if category.strip():
        query_terms_all.append(f"cat:{category.strip()}")
    if not query_terms_all: raise ValueError("No search query provided")
    query_string = " AND ".join(query_terms_all)

    client = arxiv.Client(page_size=page_size, delay_seconds=3, num_retries=3)
    search = arxiv.Search(
        query=query_string,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    def get_url_to_abstract(links) -> str:
        url = None
        for value in links:
            if type(value) == arxiv.Result.Link:
                value = value.href
                if value.startswith("http://arxiv.org/abs/") or value.startswith("https://arxiv.org/abs/"):
                    url = value
                    break
        if url is None:
            print(result)
            raise ValueError("No URL to abstract found in the result")
        return url

    new_papers: list[dict] = []
    counter = 0
    for result in client.results(search):
        paper_id = str(result.entry_id).split('/')[-1]
        if paper_id not in known_papers:
            paper = {
                "paper_id": paper_id,
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "comment": result.comment,
                "categories": result.categories,
                "published": result.published.strftime("%Y-%m-%d %H:%M:%S"),
                "updated": result.updated.strftime("%Y-%m-%d %H:%M:%S"),
                "url_abstract": get_url_to_abstract(result.links),
                "url_pdf": result.pdf_url,
                "url_links": [str(link) for link in result.links],
            }
            counter += 1
            print(f"{counter}: [{str(paper['published']).split(' ')[0]}]", paper["title"])
            new_papers.append(paper)
    return new_papers


def main(data_dir: str, category: str, old_papers: set[str], query_terms: list[str]) -> None:
    # Set up file paths and directories
    category_dir = os.path.join(data_dir, category)
    os.makedirs(category_dir, exist_ok=True)  # Ensure the category directory exists

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    new_papers_file = os.path.join(category_dir, f"{timestamp}.json")

    max_results = 1000
    if not old_papers: max_results = 10000  # maximises the number of results to fetch on the first run
    page_size = max(100, max_results // 10)

    new_papers = fetch_new_papers_using_arxiv_client(
        query_terms=query_terms,
        category=category,
        known_papers=old_papers,
        max_results=max_results,
        page_size=page_size,
    )
    update_known_papers(old_papers, new_papers)

    # Print new papers to the terminal
    if new_papers:
        print("Found:", len(new_papers), f"new papers in {category}")
        save_json(new_papers, new_papers_file)
        print(f"Saved new papers to {new_papers_file}")
    else:
        print("No new papers found.")


# Run the script
if __name__ == "__main__":
    # Load previously discovered papers
    base_data_dir = os.getenv("DATA_DIR", "/data")
    known_papers = load_known_papers(base_data_dir)
    query_terms = ["Agent", "LLM"]
    search_categories = ["cs.AI", "cs.CL", "cs.CV", 'cs.LG', 'stat.ML', 'cs.SE']  # limit search to specific categories
    search_categories = ['']  # don't limit search to specific categories
    for publication_category in search_categories:
        main(
            data_dir=base_data_dir,
            category=publication_category,
            old_papers=known_papers,
            query_terms=query_terms,
        )
    save_known_papers(known_papers, base_data_dir)
