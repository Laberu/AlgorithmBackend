#!/bin/bash

# Set the script to exit on any error
set -e

# Pull the latest changes from the repository
echo "Pulling latest changes from Git..."
git fetch origin
git reset --hard origin/main

echo "Bringing down Docker containers..."
docker-compose down

echo "Starting Docker containers in detached mode..."
docker-compose up -d

echo "Deployment complete!"

# Make the script executable with:
# chmod +x deploy.sh

# Then run it with:
# ./deploy.sh