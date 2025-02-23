# Use a minimal Python 3.11 image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the script into the container
COPY arxiv_tracker.py /app/arxiv_tracker.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Run the script as the entrypoint
ENTRYPOINT ["python", "/app/arxiv_tracker.py"]
