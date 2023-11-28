#!/bin/sh

# Create a directory to store logs
mkdir -p /github/workspace/logs

# Copy the entire workspace to the logs directory excluding the logs directory
find /github/workspace -mindepth 1 -maxdepth 1 -name logs -prune -o -exec cp -R '{}' /github/workspace/logs \;
