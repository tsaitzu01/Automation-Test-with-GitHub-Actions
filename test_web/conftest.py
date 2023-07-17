import pytest
import allure
import os
import pymysql
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

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
    cursor = cnx.cursor()

    yield cursor

    cursor.close()
    cnx.close()