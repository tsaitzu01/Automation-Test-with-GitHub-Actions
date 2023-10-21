# Stylish Automation Test Project

## About this project
1. This is an Automation Test Project for an e-commerce development project - Stylish (Owned by AppWorks School).
   - Stylish Website: http://54.201.140.239/
   - [System Requirement](https://docs.google.com/document/d/1TBzeYw5d7_tCm2sOBFECJRcBPvrPXgTrOVaCms6o3AM/edit)
   - [Stylish API Document](https://app.swaggerhub.com/apis-docs/YINGNTY/Stylish/1.0.0)
2. Included both Web UI Test and API Test.
3. The Framework is PyTest and Selenium.
4. Incorporated parallel test execution to improve efficiency

## How to execute this automation test
Please follow the steps below:
### 1. Set Environment Variables
First, you need to configure the environment variables according to the descriptions provided in the `.env-template` file. You can make a copy of the `.env-template` and name it `.env`, then set the values for the parameters.
```
cp .env-template .env
# Edit the .env file to set the values for the parameters
```
### 2. Install Required Packages
Execute the following command to install the necessary Python packages. This will install the required packages based on the dependencies listed in the `requirements.txt` file.
```
pip install -r requirements.txt
```
### 3. Run the Tests
Run the tests using pytest, specifying the name of the test file. Ensure that you have correctly set the environment variables and installed the required packages.
- Normal Test
  ```
  pytest ./test_api
  ```
  ```
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
