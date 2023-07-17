import logging
import allure
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class AdminPage(PageBase):

    # Element
    create_product_btn = (By.XPATH, "//button[text()='Create New Product']")
    product_name_list = (By.XPATH, "//td[@id='product_title']")

    category_selector = (By.XPATH, "//select[@name='category']")
    description_textarea = (By.XPATH, "//textarea[@name='description']")
    main_image_file = (By.XPATH, "//input[@name='main_image']")
    other_images_file = (By.XPATH, "//input[@name='other_images']")
    create_btn = (By.XPATH, "//input[@type='submit']")

    def new_product_info_field(self, field_name):
        field_column_name_mapping = {
            'Title': 'title',
            'Price': 'price',
            'Texture': 'texture',
            'Wash': 'wash',
            'Place of Product':'place',
            'Note':'note',
            'Story': 'story'
        }
        return (By.XPATH, f"//input[@name='{field_column_name_mapping[field_name]}']")
    
    def color_checkbox(self, color_id):
        return (By.XPATH, f"//input[@name='color_ids' and @value='{color_id}']")
    
    def size_checkbox(self, size):
        return (By.XPATH, f"//input[@name='sizes' and @value='{size}']")
    
    def delete_btn(self, product_name):
        return (By.XPATH, f"//td[text()='{product_name}']/following-sibling::td/child::button")

    # Function
    ## Click
    def click_create_product_btn(self):
        logging.info("Log: Start to click Create New Product button")
        self.find_element(self.create_product_btn, clickable = True).click()

    def click_delete_button(self, product_name):
        try:
            logging.info(f"Log: Start to click delete button of {product_name}")
            self.find_element(self.delete_btn(product_name), clickable = True).click()
        except:
            logging.info(f"Can't find the element of {product_name}")
            return "Not Found"

    def click_color_checkbox(self, colors):
        option_value_mapping = {
            '白色': '1',
            '亮綠': '2',
            '淺灰': '3',
            '淺棕': '4',
            '淺藍': '5',
            '深藍': '6',
            '粉紅': '7'
        }
        logging.info("Log: Start to click color checkbox")
        try:
            for i in colors:
                self.find_element(self.color_checkbox(option_value_mapping[i]), clickable = True).click()
        except:
            logging.info("Color is null")
            return

    def click_size_checkbox(self, sizes):
        logging.info("Log: Start to click size checkbox")
        try:
            for i in sizes:
                self.find_element(self.size_checkbox(i), clickable = True).click()
        except:
            logging.info("Size is null")
            return

    def click_create_btn(self):
        logging.info("Log: Start to click Create button")
        self.find_element(self.create_btn, clickable = True).click()

    ## Edit
    def edit_product_category(self, category):
        logging.info(f"Log: Edit the category of the new product")
        category_selector_elem = self.find_element(self.category_selector, clickable = True)
        category_selector_elem.click()
        select = Select(category_selector_elem)
        select.select_by_visible_text(category)

    ## Input
    def input_description(self, text):
        logging.info(f"Log: Input description: {text}")
        input_field_elem = self.find_element(self.description_textarea, clickable = True)
        self.input_text(input_field_elem, text)

    def input_new_product_info(self, field_name, text):
        logging.info(f"Log: Input {field_name}: {text}")
        input_field_elem = self.find_element(self.new_product_info_field(field_name), clickable = True)
        self.input_text(input_field_elem, text)

    def input_main_image(self, image):
        try:
            logging.info(f"Log: Start to input main image: {image}")
            self.find_element(self.main_image_file, clickable = True).send_keys(image)
        except:
            logging.info("There is no Main image attached")
            return

    def input_other_images(self, images):
        for index, elem in enumerate(self.find_elements(self.other_images_file)):
            if images[index] != '':
                logging.info(f"Log: Start to input other image {index}: {images[index]}")
                elem.send_keys(images[index])

    # Get
    def get_product_name_list(self):
        logging.info("Log: Start to get product name list")
        return [item.text for item in self.find_elements(self.product_name_list)]

    # General
    def fill_create_product_info(self, test_data):
        with allure.step("Select product category"):
            self.edit_product_category(test_data['Category'])

        with allure.step("Input description"):
            self.input_description(test_data['Description'])

        with allure.step("Input new product information"):
            for i in ['Title', 'Price', 'Texture', 'Wash', 'Place of Product', 'Note', 'Story']:
                self.input_new_product_info(i, test_data[i])
        
        with allure.step("Click color checkbox"):
            self.click_color_checkbox(test_data['Colors'])

        with allure.step("Click size checkbox"):
            self.click_size_checkbox(test_data['Sizes'])

        with allure.step("Input main image"):
            self.input_main_image(test_data['Main Image'])

        with allure.step("Input other images"):
            self.input_other_images([test_data['Other Image 1'], test_data['Other Image 2']])

        with allure.step("Click Create button"):
            self.click_create_btn()