#!/bin/sh

# Create a directory to store logs
mkdir -p /github/workspace/logs

# Copy the entire workspace to the logs directory excluding the logs directory
rsync -a --exclude=logs /github/workspace/ /github/workspace/logs
