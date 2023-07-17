import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options = options)
wait = WebDriverWait(driver, 10)

logo = '//a[contains(@class, "logo")]'

@allure.feature('check if logo is displayed')
def test_logo_is_display():
    try:
        logger.info('Logged INFO message')
        driver.get('http://54.201.140.239/')
        get_logo = wait.until(EC.presence_of_element_located(
            (By.XPATH, logo)
        ))

        assert get_logo
        allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)
    finally:
        driver.quit()