import logging
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class ProductPage(PageBase):

    # Element
    quantity_editor = (By.XPATH, "//div[@class='product__quantity-value']")

    # Function
    def click_product_color(self, color_code):
        logging.info(f"Log: Start to select the color: {color_code}")
        self.find_element(
            (By.XPATH, f"//div[contains(@data_id, 'color_code_{color_code}')]"), clickable = True
        ).click()

    def get_selected_color_code(self):
        selected_color_elem = self.find_element(
            (By.XPATH, "//div[contains(@class,'product__color--selected')]"), clickable = True
        )
        return selected_color_elem.get_attribute("data_id")[-6:]

    def click_product_size(self, size):
        logging.info(f"Log: Start to select the size: {size}")
        self.find_element(
            (By.XPATH, f"//div[contains(@class, 'product__size') and text() = '{size}']"), clickable = True
        ).click()

    def get_selected_size(self):
        return self.find_element(
            (By.XPATH, "//div[contains(@class,'product__size--selected')]"), clickable = True
        ).text

    def get_product_quantity(self):
        logging.info(f"Log: Start to get product quantity")
        return self.find_element(self.quantity_editor, clickable = False).text
    
    def edit_product_quantity(self, selector, times: int):
        assert selector in ["minus", "add"], \
            f"Argument for edit_product_quality function should be 'minus' or 'add'. {selector} is invalid value" 
        logging.info(f"Log: Start to {selector} {times} quantity")           
        for i in range(times):
            self.find_element(
                (By.XPATH, f"//div[contains(@class, 'product__quantity-{selector}')]"), clickable = True
            ).click()

    def click_add_to_cart_btn(self):
        logging.info("Log: Start to click add to cart button")
        self.find_element(
            (By.XPATH, "//button[contains(@class, 'add-to-cart-button')]"), clickable = True
        ).click()

    def get_cart_icon_number(self):
        return self.find_element(
            (By.XPATH, "//div[contains(@class, 'icon-cart-number')]"), clickable = True
        ).text