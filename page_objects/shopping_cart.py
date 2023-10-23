import allure
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
    
    card_number_iframe = (By.XPATH, "//div[@id='card-number']/iframe")
    card_expiration_date_iframe = (By.XPATH, "//div[@id='card-expiration-date']/iframe")
    card_ccv_iframe = (By.XPATH, "//div[@id='card-ccv']/iframe")
    checkout_btn = (By.XPATH, "//button[@class='checkout-button']")
    
    def product_delete_btn(self, product_id):
        return (By.XPATH, f"//div[text()='{product_id}']/ancestor::div/child::div[@class='cart__delete-button']")
    
    def product_quantity_selector(self, product_id):
        return (By.XPATH, f"//div[text()='{product_id}']/ancestor::div/descendant::select[@class='cart__item-quantity-selector']")
    
    def order_info_field(self, field_name):
        field_column_name_mapping = {
            'Receiver': '收件人姓名',
            'Email': 'Email',
            'Mobile': '手機',
            'Address': '地址'
        }
        return (By.XPATH, f"//div[text()='{field_column_name_mapping[field_name]}']/following-sibling::input")
    
    def deliver_time_option(self, option):
        option_column_name_mapping = {
            'Anytime': '不指定',
            'Morning': '08:00-12:00',
            'Afternoon': '14:00-18:00'
        }
        return (By.XPATH, f"//label[text()='{option_column_name_mapping[option]}']")
    
    def payment_info_field(self, field_name):
        field_column_name_mapping = {
            'Credit Card No': ['card-number-form', 'cc-number'],
            'Expiry Date': ['expiration-date-form', 'cc-exp'],
            'Security Code': ['ccv-form', 'cc-ccv']
        }
        return (By.XPATH, f"//form[@id='{field_column_name_mapping[field_name][0]}']/input[@id='{field_column_name_mapping[field_name][1]}']")

    # Function
    ## Click
    def click_cart_icon_btn(self):
        logging.info("Log: Start to click cart icon button")
        self.find_element(self.cart_icon_btn, clickable = True).click()

    def click_product_delete_btn(self, product_id):
        logging.info(f"Log: Start to click delete product button for {product_id}")
        self.find_element(self.product_delete_btn(product_id), clickable = True).click()

    def click_checkout_btn(self):
        logging.info("Log: Start to click checkout button")
        self.find_element(self.checkout_btn, clickable = True).click()

    def click_deliver_time(self, option):
        logging.info("Log: Start to click deliver time")
        try:
            self.find_element(self.deliver_time_option(option), clickable = True).click()
        except:
            logging.info("Deliver Time is null")
            return

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

    ## Input
    def input_order_info(self, field_name, text):
        logging.info(f"Log: Input {field_name}: {text}")
        input_field_elem = self.find_element(self.order_info_field(field_name), clickable = True)
        self.input_text(input_field_elem, text)

    def input_payment_info(self, field_name, text):
        logging.info(f"Log: Input {field_name}: {text}")
        if field_name == 'Credit Card No':
            self.driver.switch_to.frame(self.find_element(self.card_number_iframe))
        elif field_name == 'Expiry Date':
            self.driver.switch_to.frame(self.find_element(self.card_expiration_date_iframe))
        elif field_name == 'Security Code':
            self.driver.switch_to.frame(self.find_element(self.card_ccv_iframe))
        input_field_elem = self.find_element(self.payment_info_field(field_name), clickable = True)
        self.input_text(input_field_elem, text)
        self.driver.switch_to.default_content()

    # General
    def fill_checkout_info(self, test_data):
        with allure.step("Input order infomation"):
            for i in ['Receiver', 'Email', 'Mobile', 'Address']:
                self.input_order_info(i, test_data[i])

        with allure.step("Select deliver time"):
            self.click_deliver_time(test_data['Deliver Time'])

        with allure.step("Input payment information"):
            for i in ['Credit Card No', 'Expiry Date', 'Security Code']:
                self.input_payment_info(i, test_data[i])

        with allure.step("Click checkout button"):
            self.click_checkout_btn()