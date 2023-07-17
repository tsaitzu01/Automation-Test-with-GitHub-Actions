import allure
import logging
import os
import random
from page_objects import ShoppingCart, ProductPage, CategoryPage
from .test_data.product_detail import ProductDetail

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
        product_info['color'] = ProductDetail().get_color_by_color_code(db_connection, random_color.get_attribute('data_id')[-6:])
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

@allure.feature('Shopping Cart')
@allure.story('Shopping Cart Info Correct')
def test_shopping_cart_info(driver, db_connection):

    shopping_cart = ShoppingCart(driver)
    logging.info('Log: Start to verify shopping cart info')
    cart_info = []
    
    with allure.step("Add product to shopping cart"):
        cart_info.append(add_product_to_cart(driver, db_connection))

    with allure.step("Go to shopping cart"):
        shopping_cart.click_cart_icon_btn()

    with allure.step("Verify if cart info is displayed correctly"):
        result = shopping_cart.get_cart_info()
        assert cart_info == result, \
            f"Expected: {cart_info}\nActual: {result}"
    
    logging.info('Log: End of verify color selection function')

@allure.feature('Shopping Cart')
@allure.story('Remove product from cart')
def test_remove_product(driver, db_connection):

    shopping_cart = ShoppingCart(driver)
    logging.info('Log: Start to verify remove product from cart')
    cart_info = []
    
    with allure.step("Add 2 products to shopping cart"):
        cart_info.append(add_product_to_cart(driver, db_connection))
        cart_info.append(add_product_to_cart(driver, db_connection))

    with allure.step("Go to shopping cart"):
        shopping_cart.click_cart_icon_btn()

    with allure.step("Delete a random product from shopping cart"):
        random_product = random.choice(shopping_cart.get_products_ids_in_cart())
        shopping_cart.click_product_delete_btn(random_product)

    with allure.step("Verify alert message '已刪除商品' should be shown"):
        alert_msg = shopping_cart.get_alert_message()
        assert alert_msg == "已刪除商品", \
            f"Actual: {alert_msg}"
        
    with allure.step("Verify new cart info should be updated correctly"):
        for i, dic in enumerate(cart_info):
            if dic['id'] == random_product:
                cart_info.pop(i)
        result = shopping_cart.get_cart_info()
        assert cart_info == result, \
            f"Expected: {cart_info}\nActual: {result}"
        
@allure.feature('Shopping Cart')
@allure.story('Edit quantity in cart')
def test_edit_quantity(driver, db_connection):

    shopping_cart = ShoppingCart(driver)
    logging.info('Log: Start to verify edit quantity in cart')
    cart_info = []

    with allure.step("Add product to shopping cart"):
        cart_info.append(add_product_to_cart(driver, db_connection))

    with allure.step("Go to shopping cart"):
        shopping_cart.click_cart_icon_btn()
    
    with allure.step("Edit the quantity of the product"):
        random_product = random.choice(shopping_cart.get_products_ids_in_cart())
        available_quantity = []
        for num in range(1, 10):
            if str(num) not in {d['id'] for d in cart_info}:
                available_quantity.append(num)
        random_quantity = random.choice(available_quantity)
        shopping_cart.edit_product_quantity(random_product, str(random_quantity))

    with allure.step("Verify alert message '已修改數量' should be shown"):
        alert_msg = shopping_cart.get_alert_message()
        assert alert_msg == "已修改數量", \
            f"Actual: {alert_msg}"
        
    with allure.step("Verify subtotal should be updated correctly"):
        for i, dic in enumerate(cart_info):
            if dic['id'] == random_product:
                dic['quantity'] = str(random_quantity)
                dic['subtotal'] = str(int(dic['price']) * random_quantity)

        result = shopping_cart.get_cart_info()
        assert cart_info == result, \
            f"Expected: {cart_info}\nActual: {result}"