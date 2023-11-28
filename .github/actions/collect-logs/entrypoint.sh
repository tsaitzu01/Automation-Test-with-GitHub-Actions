#!/bin/sh

mkdir -p /github/workspace/logs
find /github/workspace/allure-results -name "*.log" -exec cp {} /github/workspace/logs \;

echo "::set-output name=logs-path::/github/workspace/logs"
