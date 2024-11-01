from datetime import datetime

import feedparser
import json
import os


def load_json(filename) -> dict | list:
    if filename and os.path.exists(filename):
        with open(filename, "rt") as f:
            return json.load(f)
    return []


def save_json(papers: list | dict, filename: str) -> None:
    with open(filename, "wt") as f:
        json.dump(papers, f, indent=4)


def load_known_papers(src_dir: str) -> set[str]:
    file = os.path.join(src_dir, "found_papers.json")
    return set(load_json(file))


def update_known_papers(old_papers: set[str], new_papers: list[dict]) -> None:
    for paper in new_papers:
        old_papers.add(paper["link"])


def save_known_papers(papers: set[str], dst_dir: str) -> None:
    file = os.path.join(dst_dir, "found_papers.json")
    save_json(list(papers), file)


def fetch_new_papers(feed_url: str, known_papers: set[str]):
    """Fetch new papers from the ATOM feed based on the previous JSON file content."""
    feed = feedparser.parse(feed_url)
    new_papers = []

    for entry in feed.entries:
        if entry.link not in known_papers:
            # Extract the paper information
            paper = {
                "title": entry.title,
                "authors": [author.name for author in entry.authors],
                "summary": entry.summary,
                "published": entry.published,
                "link": entry.link
            }
            new_papers.append(paper)
    return new_papers


def main(data_dir: str, category: str, old_papers: set[str]) -> None:
    # Set up file paths and directories
    category_dir = os.path.join(data_dir, category)
    os.makedirs(category_dir, exist_ok=True)  # Ensure the category directory exists

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    new_papers_file = os.path.join(category_dir, f"{timestamp}.json")

    # URL of the arXiv ATOM feed (customize category or search query as needed)
    atom_feed_url = build_feed_query(category)

    # Fetch new papers
    new_papers = fetch_new_papers(atom_feed_url, old_papers)
    update_known_papers(old_papers, new_papers)

    # Print new papers to the terminal
    if new_papers:
        print("Found: ", len(new_papers), "new papers")
        save_json(new_papers, new_papers_file)
        print(f"Saved new papers to {new_papers_file}")
    else:
        print("No new papers found.")

def build_feed_query(category: str, start: int = 0, max_results: int = 1000) -> str:
    return f"http://export.arxiv.org/api/query?search_query=cat:{category}&start={start}&max_results={max_results}"

# Run the script
if __name__ == "__main__":
    # Load previously discovered papers
    base_data_dir = os.getenv("DATA_DIR", "/data")
    known_papers = load_known_papers(base_data_dir)
    for publication_category in ["cs.AI", "cs.CL", "cs.CV", 'cs.LG', 'stat.ML']:
        main(data_dir=base_data_dir, category=publication_category, old_papers=known_papers)
    save_known_papers(known_papers, base_data_dir)
