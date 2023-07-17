import logging
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class ShoppingCart(PageBase):

    # Element
    cart_icon_btn = (By.XPATH, "//div[@class='header__link-icon-cart']")
    products_titles = (By.XPATH, "//div[@class='cart__item-name']")
    products_ids = (By.XPATH, "//div[@class='cart__item-id']")
    products_colors = (By.XPATH, "//div[@class='cart__item-color']")
    products_sizes = (By.XPATH, "//div[@class='cart__item-size']")
    products_quantity_selectors = (By.XPATH, "//select[@class='cart__item-quantity-selector']")
    products_prices = (By.XPATH, "//div[@class='cart__item-price-content']")
    products_subtotals = (By.XPATH, "//div[@class='cart__item-subtotal-content']")
    
    def product_delete_btn(self, product_id):
        return (By.XPATH, f"//div[text()='{product_id}']/ancestor::div/child::div[@class='cart__delete-button']")
    
    def product_quantity_selector(self, product_id):
        return (By.XPATH, f"//div[text()='{product_id}']/ancestor::div/descendant::select[@class='cart__item-quantity-selector']")

    # Function
    ## Click
    def click_cart_icon_btn(self):
        logging.info("Log: Start to click cart icon button")
        self.find_element(self.cart_icon_btn, clickable = True).click()

    def click_product_delete_btn(self, product_id):
        logging.info(f"Log: Start to click delete product button for {product_id}")
        self.find_element(self.product_delete_btn(product_id), clickable = True).click()

    ## Get
    def get_products_titles_in_cart(self):
        logging.info("Log: Start to get products' titles in cart")
        return [title.text for title in self.find_elements(self.products_titles)]
    
    def get_products_ids_in_cart(self):
        logging.info("Log: Start to get products' ids in cart")
        return [id.text for id in self.find_elements(self.products_ids)]
    
    def get_products_colors_in_cart(self):
        logging.info("Log: Start to get products' colors in cart")
        return [color.text[3:] for color in self.find_elements(self.products_colors)]
    
    def get_products_sizes_in_cart(self):
        logging.info("Log: Start to get products' sizes in cart")
        return [size.text[3:] for size in self.find_elements(self.products_sizes)]
    
    def get_products_quantity_in_cart(self):
        logging.info("Log: Start to get products' quantity in cart")
        products_quantity_in_cart = []
        for quantity_selector in self.find_elements(self.products_quantity_selectors):
            selected_quantity = Select(quantity_selector).first_selected_option.text
            products_quantity_in_cart.append(selected_quantity)
        return products_quantity_in_cart

    def get_products_prices_in_cart(self):
        logging.info("Log: Start to get products' prices in cart")
        return [price.text.split(".")[1] for price in self.find_elements(self.products_prices)]
    
    def get_products_subtotals_in_cart(self):
        logging.info("Log: Start to get products' subtotals in cart")
        return [subtotal.text.split(".")[1] for subtotal in self.find_elements(self.products_subtotals)]
    
    def get_cart_info(self):
        cart_info = []
        for i in range(len(self.get_products_ids_in_cart())):
            cart_info.append({
                'title': self.get_products_titles_in_cart()[i],
                'id': self.get_products_ids_in_cart()[i],
                'color': self.get_products_colors_in_cart()[i],
                'size': self.get_products_sizes_in_cart()[i],
                'quantity': self.get_products_quantity_in_cart()[i],
                'price': self.get_products_prices_in_cart()[i],
                'subtotal': self.get_products_subtotals_in_cart()[i]
            })
        return cart_info
    
    ## Edit
    def edit_product_quantity(self, product_id, quantity):
        logging.info(f"Log: Edit the quantity of {product_id} to {quantity}")
        quantity_selector_elem = self.find_element(self.product_quantity_selector(product_id), clickable = True)
        quantity_selector_elem.click()
        select = Select(quantity_selector_elem)
        select.select_by_visible_text(quantity)