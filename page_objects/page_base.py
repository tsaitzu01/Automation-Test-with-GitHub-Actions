from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")