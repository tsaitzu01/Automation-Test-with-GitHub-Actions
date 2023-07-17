import pytest
import allure
import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from page_objects.login_page import LoginPage

if 'ENV_FILE' in os.environ:
    env_file = os.environ['ENV_FILE']
    load_dotenv(env_file)
else:
    load_dotenv()

@allure.feature()
@pytest.fixture(autouse = True)
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    yield driver
    
    allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
    driver.quit()

@pytest.fixture(scope = 'module')
def db_connection():

    cnx = pymysql.connect(
        user = os.environ.get('DB_USERNAME'), 
        password = os.environ.get('DB_PASSWORD'),
        host = os.environ.get('DB_HOST'),
        port = int(os.environ.get('DB_PORT')),
        database = os.environ.get('DB_DATABASE')
    )
    cursor = cnx.cursor(pymysql.cursors.DictCursor)

    yield cursor

    cursor.close()
    cnx.close()

@pytest.fixture()
def login(driver, request):

    login_page = LoginPage(driver)
    driver.get(os.environ.get('DOMAIN'))
    email = request.param.get("email")
    password = request.param.get("password")

    with allure.step("Member login"):
        login_page.click_profile_icon_btn()
        login_page.input_email(email)
        login_page.input_password(password)
        login_page.click_login_btn()

@pytest.fixture()
def login_success(driver):

    login_page = LoginPage(driver)
    driver.get(os.environ.get('DOMAIN'))

    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    if worker_id == 'gw0':  # Worker 1
        email = os.environ.get('EMAIL_WORKER1')
        password = os.environ.get('PASSWORD_WORKER1')
    elif worker_id == 'gw1':  # Worker 2
        email = os.environ.get('EMAIL_WORKER2')
        password = os.environ.get('PASSWORD_WORKER2')
    else:
        email = None

    with allure.step("Member login successfully"):
        login_page.click_profile_icon_btn()
        login_page.input_email(email)
        login_page.input_password(password)
        login_page.click_login_btn()

    with allure.step("Verify login success and alert message 'Login Success' should be shown"):
        alert_msg = login_page.get_alert_message()
        assert alert_msg == "Login Success", \
            f"Actual: {alert_msg}"