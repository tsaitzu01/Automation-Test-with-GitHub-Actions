import logging
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class ThankyouPage(PageBase):

    # Element
    receiver = (By.XPATH, "//div[text()='收件人: ']/following-sibling::div")
    email = (By.XPATH, "//div[text()='Email: ']/following-sibling::div")
    mobile = (By.XPATH, "//div[text()='手機: ']/following-sibling::div")
    address = (By.XPATH, "//div[text()='地址: ']/following-sibling::div")
    delivery_time = (By.XPATH, "//div[text()='配送時間: ']/following-sibling::div")

    # Function
    def get_order_info(self):
        option_column_name_mapping = {
            '不指定': 'Anytime',
            '08:00 - 12:00': 'Morning',
            '14:00 - 18:00': 'Afternoon'
        }
        return {
            'Receiver': self.find_element(self.receiver).text,
            'Email': self.find_element(self.email).text,
            'Mobile': self.find_element(self.mobile).text,
            'Address': self.find_element(self.address).text,
            'Deliver Time': option_column_name_mapping[self.find_element(self.delivery_time).text]
        }