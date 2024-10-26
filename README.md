
# arXiv Publications Tracker

This project uses a Dockerized Python script to parse the arXiv ATOM feed for new publications across specified categories (e.g., `cs.AI`, `stat.ML`). Each time the script runs, it updates JSON files with known publications and logs new publications to timestamped files in category-specific subdirectories within the shared `/data` directory.

## Features
- Parses arXiv's ATOM feed and identifies new publications across multiple categories.
- Saves all publications from each ATOM feed to category-specific directories (e.g., `data/cs.AI/`).
- Logs new publications to timestamped JSON files in the appropriate `/data/<CATEGORY>/` directory.

## Project Structure

```
├── Dockerfile               # Docker configuration to create the container environment
├── README.md                # Project documentation with setup, usage, and overview
├── arxiv_tracker.py         # Main script to track and organize arXiv publications by category
├── build_and_run.sh         # Script to build and start the Docker container
├── data                     # Directory for storing publication data by arXiv category
│   ├── cs.AI                # Data related to Artificial Intelligence publications
│   ├── cs.CL                # Data related to Computation and Language (NLP) publications
│   ├── cs.CV                # Data related to Computer Vision publications
│   ├── cs.LG                # Data related to Machine Learning publications
│   └── stat.ML              # Data related to Statistics - Machine Learning publications
├── destroy.sh               # Script to stop and remove the Docker container for cleanup
├── docker-compose.yml       # Docker Compose configuration file for managing services
└── requirements.txt         # List of required Python packages for the project
```
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

