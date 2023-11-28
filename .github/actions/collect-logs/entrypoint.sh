#!/bin/sh

mkdir -p /github/workspace/logs
cp -R /github/workspace/allure-results /github/workspace/logs

echo "::set-output name=logs-path::/github/workspace/logs"
