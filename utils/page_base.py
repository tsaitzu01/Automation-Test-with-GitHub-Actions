import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class PageBase:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, locator, clickable = False):
        if clickable:
            elem = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
        else:
            elem = self.wait.until(
                EC.presence_of_element_located(locator)
            )
        return elem
    
    def find_elements(self, locator):
        elem = self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )
        return elem
    
    def input_text(self, elem, text):
        elem.clear()
        elem.send_keys(text)

    def press_enter(self, elem):
        elem.send_keys(Keys.ENTER)

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def find_alert_element(self):
        return self.wait.until(EC.alert_is_present())
    
    def get_alert_message(self):
        logging.info("Start to get alert message")
        self.find_alert_element()
        return self.driver.switch_to.alert.text
    
    def accept_alert(self):
        logging.info("Start to accept alert")
        self.find_alert_element()
        self.driver.switch_to.alert.accept()