import feedparser
import json
import os
from datetime import datetime


def load_existing_papers(file_path):
    """Load the existing papers from the JSON file, if it exists."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []


def save_papers(papers, file_path):
    """Save the list of papers to the JSON file."""
    with open(file_path, "w") as f:
        json.dump(papers, f, indent=4)


def fetch_new_papers(feed_url, existing_titles):
    """Fetch new papers from the ATOM feed that aren't in existing_titles."""
    feed = feedparser.parse(feed_url)
    new_papers = []
    for entry in feed.entries:
        if entry.title not in existing_titles:
            paper = {
                "title": entry.title,
                "authors": [author.name for author in entry.authors],
                "summary": entry.summary,
                "published": entry.published,
                "link": entry.link
            }
            new_papers.append(paper)
    return new_papers


def main(search_category):
    # Set up file paths and directories
    data_dir = os.getenv("DATA_DIR", "/data")
    known_papers_file = os.path.join(data_dir, "arxiv_papers.json")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    new_papers_file = os.path.join(data_dir, f"{timestamp}.json")

    # Load existing papers
    existing_papers = load_existing_papers(known_papers_file)
    existing_titles = {paper["title"] for paper in existing_papers}

    # URL of the arXiv ATOM feed (customize category or search query as needed)
    atom_feed_url = f"http://export.arxiv.org/api/query?search_query=cat:{search_category}&start=0&max_results=1000"

    # Fetch new papers
    new_papers = fetch_new_papers(atom_feed_url, existing_titles)

    # Print new papers to the terminal
    if new_papers:
        print("New papers found:")
        for paper in new_papers:
            print(f"Title: {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            print(f"Published: {paper['published']}")
            print(f"Link: {paper['link']}\n")
    else:
        print("No new papers found.")

    # Save new papers to a timestamped file and update known papers file
    if new_papers:
        save_papers(new_papers, new_papers_file)
        print(f"Saved new papers to {new_papers_file}")

    # Update the list of known papers and save
    all_papers = existing_papers + new_papers
    save_papers(all_papers, known_papers_file)
    print(f"Updated {known_papers_file} with {len(new_papers)} new papers.")


# Run the script
if __name__ == "__main__":
    search_category = "cs.AI"
    main(search_category)
