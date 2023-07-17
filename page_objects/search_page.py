from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class SearchPage(PageBase):

    # Element
    search_field = (By.XPATH, "//input[contains(@class, 'header__search')]")
    search_result_title = (By.XPATH, "//div[contains(@class,'product__title')]")
   
    # Function
    def __init__(self, driver):
        super().__init__(driver)
        self.search_field_elem = self.find_element(self.search_field, clickable = True)

    def input_search_keyword(self, keyword):
        self.input_text(self.search_field_elem, keyword)

    def send_search_keyword(self):
        self.press_enter(self.search_field_elem)

    def get_search_results(self):
        current_search_results = []
        while True:
            self.scroll_down()
            try:
                self.find_element(
                    (By.XPATH, f"//div[@class='products' and count(a) > {len(current_search_results)}]")
                )
                current_search_results = self.find_elements(self.search_result_title)
            except:
                return current_search_results