import allure
import logging
import os
from page_objects.product_page import ProductPage
from page_objects.category_page import CategoryPage

product_id = '201807201824'

def enter_product_page_from_category_page(driver):

    driver.get(os.environ.get('DOMAIN'))
    logging.info(f'Log: Start to select product from Category Page: Select {product_id}')
    category_page = CategoryPage(driver)
    category_page.click_product(product_id)

@allure.feature('Product Page Related Feature - Color Selection')
def test_product_color_selection(driver):
    color_code = 'DDFFBB'

    logging.info(f'Log: Start to verify color selection function: Select {color_code} for {product_id}')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    product_page.click_product_color(color_code)

    logging.info("Log: Start to verify if the selected color is highlighted")
    assert color_code == product_page.get_selected_color_code(), \
        f"Expected: {color_code}, Actual: {product_page.get_selected_color_code()}"
    logging.info('Log: End of verify color selection function')
    
@allure.feature('Product Page Related Feature - Size Selection')
def test_product_size_selection(driver):
    size = 'M'

    logging.info(f'Log: Start to verify color selection function: Select {size} for {product_id}')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    product_page.click_product_size(size)

    logging.info("Log: Start to verify if the selected size is highlighted")
    assert size == product_page.get_selected_size(), \
        f"Expected: {size}, Actual: {product_page.get_selected_size()}"
    logging.info('Log: End of verify size selection function')

@allure.feature('Product Page Related Feature - Quantity Editor Disabled')
def test_quantity_editor_disabled(driver):

    logging.info(f'Log: Start to verify quantity editor disabled')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    expected = product_page.get_product_quantity()
    logging.info(f"Log: The original product quantity is: {expected}")

    product_page.edit_product_quantity('add', 2)
    result = product_page.get_product_quantity()
    logging.info(f"Log: The new product quantity is: {result}")

    logging.info("Log: Start to verify if quantity editor is disabled")
    assert expected == result, \
        f"Expected: {expected}\nActual: {result}"
    logging.info('Log: End of verify quantity editor disabled')

@allure.feature('Product Page Related Feature - Quantity Editor - Increase Quantity')
def test_increase_quantity(driver):
    size = 'M'
    edit_quantity_times = 8

    logging.info(f'Log: Start to verify increase quantity')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    product_page.click_product_size(size)
    original_quantity = int(product_page.get_product_quantity())
    
    product_page.edit_product_quantity('add', edit_quantity_times)
    
    logging.info("Log: Start to verify quantity is added")
    expected = original_quantity + edit_quantity_times
    assert expected == int(product_page.get_product_quantity()), \
        f"Expected: {expected}\nActual: {product_page.get_product_quantity()}"

    edit_quantity_times = 2
    product_page.edit_product_quantity('add', edit_quantity_times)

    logging.info("Log: Start to verify quantity would not more than 9")
    assert expected == int(product_page.get_product_quantity()), \
        f"Expected: {expected}\nActual: {int(product_page.get_product_quantity())}"
    logging.info('Log: End of verify increase quantity')
    
@allure.feature('Product Page Related Feature - Quantity Editor - Decrease Quantity')
def test_decrease_quantity(driver):
    size = 'M'
    edit_quantity_times = 8

    logging.info(f'Log: Start to verify dncrease quantity')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    product_page.click_product_size(size)
    original_quantity = int(product_page.get_product_quantity())
    
    product_page.edit_product_quantity('add', edit_quantity_times)

    product_page.edit_product_quantity('minus', edit_quantity_times)

    logging.info("Log: Start to verify quantity is decreased")
    assert original_quantity == int(product_page.get_product_quantity()), \
        f"Expected: {original_quantity}\nActual: {int(product_page.get_product_quantity())}"
    logging.info('Log: End of verify dncrease quantity')
       
@allure.feature('Product Page Related Feature - Add To Cart - Success')
def test_add_to_cart_success(driver):
    size = 'M'

    logging.info(f'Log: Start to verify add to cart - Success')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    product_page.click_product_size(size)
    original_quantity = int(product_page.get_product_quantity())

    product_page.click_add_to_cart_btn()

    logging.info("Log: Start to verify success message should be shown")
    assert "已加入購物車" == product_page.get_alert_message(), \
        f"Actual: {product_page.get_alert_message()}"

    product_page.accept_alert()

    logging.info("Log: Start to verify cart icon number is the same as product quantity")
    assert original_quantity == int(product_page.get_cart_icon_number()), \
        f"Expected: {original_quantity}\nActual: {int(product_page.get_cart_icon_number())}"
    logging.info(f'Log: End of verify add to cart - Success')
    
@allure.feature('Product Page Related Feature - Add To Cart - Failed')
def test_add_to_cart_failed(driver):

    logging.info(f'Log: Start to verify add to cart - Failed')
    enter_product_page_from_category_page(driver)

    product_page = ProductPage(driver)
    product_page.click_add_to_cart_btn()

    logging.info("Log: Start to verify alert message should be shown")
    assert "請選擇尺寸" == product_page.get_alert_message(), \
        f"Actual: {product_page.get_alert_message()}"
    
    product_page.accept_alert()
    logging.info(f'Log: End of verify add to cart - Failed')