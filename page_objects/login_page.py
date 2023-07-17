import logging
from selenium.webdriver.common.by import By
from utils.page_base import PageBase

class LoginPage(PageBase):

    # Element
    profile_icon_btn = (By.XPATH, "//div[@class='header__link-icon-profile']")
    email_textbox = (By.ID, "email")
    password_textbox = (By.ID, "pw")
    login_btn = (By.XPATH, "//button[@class='login100-form-btn']")
    logout_btn = (By.XPATH, "//button[text()='登出']")

    # Function
    ## Click
    def click_profile_icon_btn(self):
        logging.info("Log: Start to click profile icon button")
        self.find_element(self.profile_icon_btn, clickable = True).click()

    def click_login_btn(self):
        logging.info("Log: Start to click login button")
        self.find_element(self.login_btn, clickable = True).click()

    def click_logout_btn(self):
        logging.info("Log: Start to click logout button")
        self.find_element(self.logout_btn, clickable = True).click()

    ## Input
    def input_email(self, email):
        logging.info(f"Log: Input email: {email}")
        email_textbox_elem = self.find_element(self.email_textbox, clickable = True)
        self.input_text(email_textbox_elem, email)

    def input_password(self, password):
        logging.info(f"Log: Input password: {password}")
        password_textbox_elem = self.find_element(self.password_textbox, clickable = True)
        self.input_text(password_textbox_elem, password)