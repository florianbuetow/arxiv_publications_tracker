# arXiv Publications Tracker

This project uses a Dockerized Python script to parse the arXiv ATOM feed for new publications in a specified category (e.g., `cs.AI`). Each time the script runs, it updates a JSON file with known publications and logs new publications to a timestamped file in a shared `/data` directory.

## Features
- Parses arXiv's ATOM feed and identifies new publications.
- Saves all publications from the ATOM feed to `arxiv_papers.json`.
- Logs new publications to a timestamped JSON file in the `/data` directory.

## Setup Instructions

### 1. Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 2. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```
### 3. Make the scripts executable

```bash
chmod +x *.sh
```
### 4. Adjust the category you want to track by editing the the `arxiv_tracker.py` file

At the end of the file you will find the following lines:
```python
if __name__ == "__main__":
    search_category = "cs.AI"
    main(search_category)
```
Adjust the `search_category` variable to the category you want to track. You can find the list of categories [here](https://arxiv.org/category_taxonomy).

### 5. Build and run the Docker Image

```bash
./build_and_run.sh
```

### 6. Destroy the Docker Container

```bash
./destroy.sh
``` 




