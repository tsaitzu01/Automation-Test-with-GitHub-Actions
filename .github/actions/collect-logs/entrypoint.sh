#!/bin/sh

# Create a directory to store logs
mkdir -p /github/workspace/logs

# Copy the entire workspace to the logs directory excluding the logs directory
shopt -s extglob
cp -R /github/workspace/!(logs) /github/workspace/logs
