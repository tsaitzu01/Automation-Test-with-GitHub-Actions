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

    def scroll_to_element(self, elem):
        self.driver.execute_script("arguments[0].scrollIntoView();", elem)

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def get_alert_message(self):
        logging.info("Log: Start to get alert message")
        self.wait.until(EC.alert_is_present())
        alert_message = self.driver.switch_to.alert.text
        logging.info(f"Alert Message: {alert_message}")
        self.driver.switch_to.alert.accept()
        return alert_message
    
    def get_keys_of_local_storage(self):
        keys = self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")
        logging.info(f"Log: These are keys in local storage: {keys}")
        return keys

    def get_local_storage_by_key(self, key):
        value = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)
        logging.info(f"Log: The local storage of '{key}' is '{value}'")
        return value
    
    def set_local_storage(self, key, value):
        logging.info(f"Log: Set local storage key: '{key}' with value: '{value}'")
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)