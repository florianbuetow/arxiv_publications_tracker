#!/bin/bash
# Stops the containers and removes the image that was built
docker compose down arxiv_watchdog --rmi all
