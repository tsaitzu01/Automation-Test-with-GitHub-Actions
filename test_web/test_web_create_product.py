import pytest
import allure
import logging
import os
from page_objects import AdminPage
from test_data.get_data_from_excel import GetDataFromExcel

@allure.feature('Create Product')
@allure.step('Create Product Success')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_create_product('Create Product Success'))
def test_create_product_success(driver, login_success, test_data, request):

    admin_page = AdminPage(driver)
    logging.info('Log: Start to create product success')
    
    with allure.step("Go to admin page"):
        driver.get(os.environ.get('DOMAIN') + '/admin/products.html')

    with allure.step("Click 'Create New Product' button"):
        admin_page.click_create_product_btn()
        driver.switch_to.window(driver.window_handles[-1])

    with allure.step("Create product with valid values"):
        admin_page.fill_create_product_info(test_data)

    with allure.step("Verify alert message 'Create Product Success' should be shown"):
        alert_msg = admin_page.get_alert_message()
        assert alert_msg == "Create Product Success", \
            f"Actual: {alert_msg}"
        
    with allure.step("Verify new product should be displayed on product list"):
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        product_list = admin_page.get_product_name_list()
        assert test_data['Title'] in product_list, \
            f"{test_data['Title']} isn't in product list.\nProduct list: {product_list}"
        allure.attach(driver.get_screenshot_as_png(), name='screenshot', attachment_type=allure.attachment_type.PNG)

    def finalizer():
        with allure.step("Reset the data in a database: delete product"):
            if admin_page.click_delete_button(test_data['Title']) == "True":
                with allure.step("Verify alert message 'Delete Product Success' should be shown"):
                    alert_msg = admin_page.get_alert_message()
                    assert alert_msg == "Delete Product Success", f"Actual: {alert_msg}"
        
    request.addfinalizer(finalizer)
        
@allure.feature('Create Product')
@allure.step('Create Product with Invalid Value')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_create_product('Create Product Failed'))
def test_create_product_fail(driver, login_success, test_data, request):

    admin_page = AdminPage(driver)
    logging.info('Log: Start to create product with invalid value')
    
    with allure.step("Go to admin page"):
        driver.get(os.environ.get('DOMAIN') + '/admin/products.html')

    with allure.step("Click 'Create New Product' button"):
        admin_page.click_create_product_btn()
        driver.switch_to.window(driver.window_handles[-1])

    with allure.step("Create product with invalid values"):
        admin_page.fill_create_product_info(test_data)
  
    with allure.step("Verify related alert message should be shown"):
        alert_msg = admin_page.get_alert_message()
        assert alert_msg == test_data['Alert Msg'], \
            f"Actual: {alert_msg}"
        
    def finalizer():
        with allure.step("Reset the data in a database: delete product"):
            if admin_page.click_delete_button(test_data['Title']) == "True":
                with allure.step("Verify alert message 'Delete Product Success' should be shown"):
                    alert_msg = admin_page.get_alert_message()
                    assert alert_msg == "Delete Product Success", f"Actual: {alert_msg}"
        
    request.addfinalizer(finalizer)
        
@allure.feature('Create Product')
@allure.step('Create Product without login')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_create_product('Create Product Success'))
def test_create_product_without_login(driver, test_data):

    admin_page = AdminPage(driver)
    logging.info('Log: Start to create product without login')
    
    with allure.step("Go to product create page"):
        driver.get(os.environ.get('DOMAIN') + '/admin/product_create.html')

    with allure.step("Create product with valid values"):
        admin_page.fill_create_product_info(test_data)

    with allure.step("Verify alert message 'Please Login First' should be shown"):
        alert_msg = admin_page.get_alert_message()
        assert alert_msg == "Please Login First", \
            f"Actual: {alert_msg}"

    with allure.step("Verify website should be redirected to login page"):
        assert driver.current_url == os.environ.get('DOMAIN') + '/login.html'