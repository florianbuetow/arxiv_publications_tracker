import feedparser
import json
import os
from datetime import datetime

def load_papers(file_path):
    """Load list of papers from the JSON file, if it exists."""
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_papers(papers, file_path):
    """Save the list of papers to the JSON file."""
    with open(file_path, "w") as f:
        json.dump(papers, f, indent=4)

def fetch_new_papers(feed_url, existing_papers):
    """Fetch new papers from the ATOM feed based on the previous JSON file content."""
    feed = feedparser.parse(feed_url)
    existing_links = {paper["link"] for paper in existing_papers}
    new_papers = []

    for entry in feed.entries:
        # Stop if the paper link already exists in the saved papers
        if entry.link in existing_links:
            break
        paper = {
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "summary": entry.summary,
            "published": entry.published,
            "link": entry.link
        }
        new_papers.append(paper)

    return new_papers

def find_last_json_file(data_dir):
    files = os.listdir(data_dir)
    json_files = [f for f in files if f.endswith(".json")]
    if json_files:
        return os.path.join(data_dir, max(json_files))
    return None

def main(search_category):
    # Set up file paths and directories
    base_data_dir = os.getenv("DATA_DIR", "/data")
    category_dir = os.path.join(base_data_dir, search_category)
    os.makedirs(category_dir, exist_ok=True)  # Ensure the category directory exists

    previous_papers_file = find_last_json_file(category_dir)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    new_papers_file = os.path.join(category_dir, f"{timestamp}.json")

    # Load existing papers
    existing_papers = load_papers(previous_papers_file)

    # URL of the arXiv ATOM feed (customize category or search query as needed)
    atom_feed_url = f"http://export.arxiv.org/api/query?search_query=cat:{search_category}&start=0&max_results=1000"

    # Fetch new papers
    new_papers = fetch_new_papers(atom_feed_url, existing_papers)

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

# Run the script
if __name__ == "__main__":
    for search_category in ["cs.AI", "cs.CL", "cs.CV", 'cs.LG', 'stat.ML']:
        main(search_category)
