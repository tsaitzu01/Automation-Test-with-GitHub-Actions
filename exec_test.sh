#!/bin/sh

# Create virtual environment
python3 -m venv venv
# Enter virtual environment
source venv/bin/activate
# Install all python plugin needed
pip install -r requirement.txt
# Execute test_sample.py and generate allure report
# pytest ./test_web/test_web_$1.py
pytest --reruns 3 --reruns-delay 2 ./test_web
pytest --reruns 3 --reruns-delay 2 ./test_api