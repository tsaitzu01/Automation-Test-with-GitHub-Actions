import allure
import pytest
import requests
import os
import logging
from dotenv import load_dotenv
from api_objects import UserLoginAPI

if 'ENV_FILE' in os.environ:
    env_file = os.environ['ENV_FILE']
    load_dotenv(env_file)
else:
    load_dotenv()

@allure.feature()
@pytest.fixture(autouse = True)
def session():
    session = requests.session()
    
    yield session

@pytest.fixture()
def login(session, request): 
    
    email = request.param.get("email")
    password = request.param.get("password")

    user_login_api = UserLoginAPI(session, email=email, password=password)

    with allure.step("Member login"):
        yield user_login_api.send_login()

@pytest.fixture()
def login_success(session):

    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    if worker_id == 'gw0':  # Worker 1
        email = os.environ.get('EMAIL_WORKER1')
        password = os.environ.get('PASSWORD_WORKER1')
    elif worker_id == 'gw1':  # Worker 2
        email = os.environ.get('EMAIL_WORKER2')
        password = os.environ.get('PASSWORD_WORKER2')
    else:
        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')

    user_login_api = UserLoginAPI(session, email=email, password=password)

    with allure.step("Member login successfully"):
        logging.info("Log: Start to login")
        login = user_login_api.send_login()
        
    with allure.step("Save access token in the Header"):
        logging.info("Log: Start to save access token in the Header")
        session.headers["Authorization"] = f"Bearer {user_login_api.get_response_body()['data']['access_token']}"

    return login