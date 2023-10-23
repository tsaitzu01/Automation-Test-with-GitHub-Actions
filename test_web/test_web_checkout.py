import pytest
import allure
import logging
import random
import os
from page_objects import ShoppingCart, ProductPage, CategoryPage, ThankyouPage
from db_query import DbQuery
from test_data.get_data_from_excel import GetDataFromExcel

def add_product_to_cart(driver, db_connection):
    driver.get(os.environ.get('DOMAIN'))
    category_page = CategoryPage(driver)
    product_page = ProductPage(driver)
    product_info = {}

    with allure.step("Select random product from Category Page"):
        random_product = random.choice(category_page.get_product_list())
        product_info['title'] = random_product.text
        category_page.click_product(random_product)

    with allure.step("Select a color of the product"):
        random_color = random.choice(product_page.get_all_colors())
        product_info['color'] = DbQuery().get_color_by_color_code(db_connection, random_color.get_attribute('data_id')[-6:])
        product_page.click_product_color(random_color)

    with allure.step("Select a size of the product"):
        random_size = random.choice(product_page.get_all_sizes())
        product_info['size'] = random_size.text
        product_page.click_product_size(random_size)

    with allure.step("Get product info"):
        product_info['id'] = product_page.get_product_id()
        product_info['price'] = product_page.get_product_price()
        product_info['quantity'] = product_page.get_product_quantity()
        product_info['subtotal'] = str(int(product_page.get_product_price()) * int(product_page.get_product_quantity()))

    with allure.step("Click add to cart button"):
        product_page.click_add_to_cart_btn()
        product_page.get_alert_message()

    return product_info

@allure.feature('Checkout')
@allure.step('Checkout with empty cart')
def test_checkout_with_empty_cart(driver, login_success):

    shopping_cart = ShoppingCart(driver)
    logging.info('Log: Start to checkout with empty cart')
    
    with allure.step("Go to shopping cart page"):
        driver.get(os.environ.get('DOMAIN') + '/cart.html')

    with allure.step("Click checkout button without add product to shopping cart"):
        shopping_cart.click_checkout_btn()

    with allure.step("Verify alert message '尚未選購商品' should be shown"):
        alert_msg = shopping_cart.get_alert_message()
        assert alert_msg == "尚未選購商品", \
            f"Actual: {alert_msg}"
        
@allure.feature('Checkout')
@allure.step('Checkout with invalid values')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_checkout_value('Checkout with Invalid Value'))
def test_checkout_with_invalid_values(driver, db_connection, login_success, test_data):

    shopping_cart = ShoppingCart(driver)
    logging.info('Log: Start to checkout with invalid values')

    with allure.step("Add product to shopping cart"):
        add_product_to_cart(driver, db_connection)

    with allure.step("Go to shopping cart page"):
        shopping_cart.click_cart_icon_btn()

    with allure.step("Fill in invalid value to checkout"):
        shopping_cart.fill_checkout_info(test_data)

    with allure.step("Verify related alert message should be shown"):
        alert_msg = shopping_cart.get_alert_message()
        assert alert_msg == test_data['Alert Msg'], \
            f"Actual: {alert_msg}"
            
@allure.feature('Checkout')
@allure.step('Checkout with valid values')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_checkout_value('Checkout with Valid Value'))
def test_checkout_with_valid_values(driver, db_connection, login_success, test_data):

    shopping_cart = ShoppingCart(driver)
    thankyou_page = ThankyouPage(driver)
    logging.info('Log: Start to checkout with valid values')

    with allure.step("Add product to shopping cart"):
        add_product_to_cart(driver, db_connection)

    with allure.step("Go to shopping cart page"):
        shopping_cart.click_cart_icon_btn()
        
    with allure.step("Fill in valid value to checkout"):
        shopping_cart.fill_checkout_info(test_data)

    with allure.step("Verify alert message '付款成功' should be shown"):
        alert_msg = shopping_cart.get_alert_message()
        assert alert_msg == "付款成功", \
            f"Actual: {alert_msg}"
            
    with allure.step("Verify correct order info should be displayed in thankyou page"):
        expected = {}
        for i in ['Receiver', 'Email', 'Mobile', 'Address', 'Deliver Time']:
            expected[i] = test_data[i]
        results = thankyou_page.get_order_info()
        assert results == expected, \
            f"Expected: {expected}, Actual: {results}"