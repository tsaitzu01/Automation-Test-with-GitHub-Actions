import pytest
import allure
import os
from page_objects import LoginPage

@allure.feature('Login and Logout')
@allure.story('Login and Logout Success')
@pytest.mark.parametrize("login", [{"email": os.environ.get('EMAIL'), "password": os.environ.get('PASSWORD')}], indirect=True)
def test_login_logout_success(driver, login):

    login_page = LoginPage(driver)

    with allure.step("Verify login success and alert message 'Login Success' should be shown"):
        alert_msg = login_page.get_alert_message()
        assert alert_msg == "Login Success", \
            f"Actual: {alert_msg}"
        
    with allure.step("Verify jwt token is in local storage"):
        assert "jwtToken" in login_page.get_keys_of_local_storage(), \
            f"Can't find jwt token in local storage"

    with allure.step("Member logout"):
        login_page.click_logout_btn()

    with allure.step("Verify logout success and alert message 'Logout Success' should be shown"):
        alert_msg = login_page.get_alert_message()
        assert alert_msg == "Logout Success", \
            f"Actual: {alert_msg}"
        
    with allure.step("Verify jwt token isn't in local storage"):
        assert "jwtToken" not in login_page.get_keys_of_local_storage(), \
            f"Can't find jwt token in local storage"

@allure.feature('Login and Logout')
@allure.story('Login Failed with incorrect email or password')
@pytest.mark.parametrize("login", [{"email": "kathyfail@gmail", "password": "fail"}], indirect=True)
def test_login_logout_failed(driver, login):

    login_page = LoginPage(driver)

    with allure.step("Verify login failed and alert message 'Login Failed' should be shown"):
        alert_msg = login_page.get_alert_message()
        assert alert_msg == "Login Failed", \
            f"Actual: {alert_msg}"
        
@allure.feature('Login and Logout')
@allure.story('Login with invalid access token')
@pytest.mark.parametrize("login", [{"email": os.environ.get('EMAIL'), "password": os.environ.get('PASSWORD')}], indirect=True)
def test_login_with_invalid_access_token(driver, login):

    login_page = LoginPage(driver)

    with allure.step("Login success and copy the jwt token"):
        login_page.get_alert_message()
        jwtToken = login_page.get_local_storage_by_key("jwtToken")

    with allure.step("Member logout and logout success"):
        login_page.click_logout_btn()
        login_page.get_alert_message()

    with allure.step("Using the jwt token to access member page"):
        login_page.set_local_storage("jwtToken", f"{jwtToken}")
        driver.get(os.environ.get('DOMAIN') + '/profile.html')

    with allure.step("Verify alert message 'Invalid Access Token' should be shown"):
        alert_msg = login_page.get_alert_message()
        assert alert_msg == "Invalid Access Token", \
            f"Actual: {alert_msg}"