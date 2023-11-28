#!/bin/sh

# Create a directory to store logs
mkdir -p /github/workspace/logs

# Copy the entire workspace to the logs directory
cp -R /github/workspace/* /github/workspace/logs
