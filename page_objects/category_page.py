import logging
import random
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class CategoryPage(PageBase):

    # Element
    product_list = (By.XPATH, f"//div[contains(@class,'product__title')]")

    def header_category_btn(self, category):
        return (By.XPATH, f"//a[text()='{category}']")
   
    # Function
    def click_header_category(self, category):
        header_category_elem = self.find_element(self.header_category_btn(category), clickable = True)
        header_category_elem.click()

    def get_product_list(self):
        current_product_list = []
        while True:
            self.scroll_down()
            try:
                self.find_element(
                    (By.XPATH, f"//div[@class='products' and count(a) > {len(current_product_list)}]")
                )
                current_product_list = self.find_elements(self.product_list)
            except:
                return current_product_list
            
    def click_product(self, random_product):
        logging.info(f'Log: Select {random_product.text}')
        self.driver.execute_script("arguments[0].click();", random_product)