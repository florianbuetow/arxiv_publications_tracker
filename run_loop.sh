#!/bin/bash
# Run the build_and_run.sh script every 6 hours.
# When you adopt this script keep in mind that you
# might have to adjust the number of max results in
# the archive.py script to avoid missing new papers.
while true; do
  ./build_and_run.sh
  echo "$(date): Sleeping for 6 hours ..."
  sleep 21600
done
