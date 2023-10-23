import logging
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class ProductPage(PageBase):

    # Element
    color_selectors = (By.XPATH, "//div[contains(@class, 'product__color-selector')]/child::*")
    size_selectors = (By.XPATH, "//div[contains(@class, 'product__size')]/child::*")
    product_id = (By.XPATH, "//div[@class='product__id']")
    product_price = (By.XPATH, "//div[@class='product__price']")
    quantity_editor = (By.XPATH, "//div[@class='product__quantity-value']")
    add_to_cart_btn = (By.XPATH, "//button[contains(@class, 'add-to-cart-button')]")
    cart_icon_number = (By.XPATH, "//div[contains(@class, 'icon-cart-number')]")

    def quantity_selector(self, selector):
        return (By.XPATH, f"//div[contains(@class, 'product__quantity-{selector}')]")

    # Function
    ## Click
    def click_product_color(self, color):
        logging.info(f"Log: Start to select the color: {color.get_attribute('data_id')[-6:]}")
        self.find_element(color, clickable = True).click()

    def click_product_size(self, size):
        logging.info(f"Log: Start to select the size: {size.text}")
        self.find_element(size, clickable = True).click()

    def click_add_to_cart_btn(self):
        logging.info("Log: Start to click add to cart button")
        self.find_element(self.add_to_cart_btn, clickable = True).click()

    ## Get
    def get_all_colors(self):
        logging.info("Log: Start to get all color codes")
        return self.find_elements(self.color_selectors)

    def get_all_sizes(self):
        logging.info("Log: Start to get all sizes")
        return self.find_elements(self.size_selectors)
    
    def get_product_id(self):
        logging.info(f"Log: Start to get product id")
        return self.find_element(self.product_id).text

    def get_product_price(self):
        logging.info(f"Log: Start to get product price")
        return self.find_element(self.product_price).text.split(".")[1]

    def get_product_quantity(self):
        logging.info(f"Log: Start to get product quantity")
        return self.find_element(self.quantity_editor, clickable = False).text
    
    def get_cart_icon_number(self):
        logging.info("Log: Start to get cart icon number")
        return self.find_element(self.cart_icon_number, clickable = True).text
    
    ## Edit
    def edit_product_quantity(self, selector, times: int):
        assert selector in ["minus", "add"], \
            f"Argument for edit_product_quality function should be 'minus' or 'add'. {selector} is invalid value" 
        logging.info(f"Log: Start to {selector} {times} quantity")           
        for i in range(times):
            self.find_element(self.quantity_selector(selector), clickable = True).click()