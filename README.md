# Stylish Automation Test Project

## About this project
1. This is an Automation Test Project for an e-commerce development project - Stylish (Owned by AppWorks School).
   - System Requirement
   - Stylish Website: http://54.201.140.239/
2. Included both Web UI Test and API Test.
3. The Framework is PyTest and Selenium.
4. Incorporated parallel test execution to improve efficiency

## How to execute this automation test
1. According to the description of the parameters in the .env-template file, modify it to a valid value.
2. Start with pytest and followed by the filename of the test project
   - Normal Test
   ```
   pytest ./test_api
   pytest ./test_api/test_api_product.py
   ```
   - Parallel Test
   ```
   pytest -n 2 ./test_api
   ```
   - Parallel Test with Rerun
   ```
   pytest -n 2 --reruns 3 --reruns-delay 2 ./test_api
   ```
