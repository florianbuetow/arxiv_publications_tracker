
# arXiv Publications Tracker

This project uses a Dockerized Python script to parse the arXiv ATOM feed for new publications across specified categories (e.g., `cs.AI`, `stat.ML`). Each time the script runs, it updates JSON files with known publications and logs new publications to timestamped files in category-specific subdirectories within the shared `/data` directory.

## Features
- Parses arXiv's ATOM feed and identifies new publications across multiple categories.
- Saves all publications from each ATOM feed to category-specific directories (e.g., `data/cs.AI/`).
- Logs new publications to timestamped JSON files in the appropriate `/data/<CATEGORY>/` directory.

## Setup Instructions

### 1. Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 2. Clone the Repository

```bash
git clone git@github.com:florianbuetow/arxiv_publications_tracker.git
cd arxiv_publications_tracker
```

### 3. Make the Scripts Executable

```bash
chmod +x *.sh
```

### 4. Set the Categories to Track

In the `arxiv_tracker.py` file, specify the categories you'd like to track. At the end of the file, you'll find the following lines:

```python
# Run the script
if __name__ == "__main__":
    for search_category in ["cs.AI", "cs.CL", "cs.CV", 'cs.LG', 'stat.ML']:
        main(search_category)
```
Update the list of `search_category` values to include each category you wish to track. For example:
You can find the full list of arXiv categories [here](https://arxiv.org/category_taxonomy).

### 5. Build and Run the Docker Image

```bash
./build_and_run.sh
```

### 6. Destroy the Docker Container

```bash
./destroy.sh
```

## Data Storage

Each category tracked will have a separate folder within the `/data` directory (e.g., `data/cs.AI/`, `data/stat.ML/`). The script saves:
- All known publications for each category in the latest JSON file in `data/<CATEGORY>/`.
- New publications logged in a timestamped JSON file each time the script runs.

