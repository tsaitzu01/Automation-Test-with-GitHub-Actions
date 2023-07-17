import allure
import logging
import os
import random
from page_objects import ProductPage, CategoryPage

def enter_product_page_from_category_page(driver):

    driver.get(os.environ.get('DOMAIN'))
    category_page = CategoryPage(driver)
    logging.info(f'Log: Start to select random product from Category Page')
    random_product = random.choice(category_page.get_product_list())
    category_page.click_product(random_product)

@allure.feature('Product Page Related Feature - Color Selection')
def test_product_color_selection(driver):

    product_page = ProductPage(driver)
    logging.info('Log: Start to verify color selection function')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Select a color of the product"):
        random_color = random.choice(product_page.get_all_colors())
        product_page.click_product_color(random_color)

    with allure.step("Verify if selected color is highlighted"):
        assert 'product__color--selected' in random_color.get_attribute('class'), \
            f"The selected color isn't highlighted"
    
    logging.info('Log: End of verify color selection function')
    
@allure.feature('Product Page Related Feature - Size Selection')
def test_product_size_selection(driver):

    product_page = ProductPage(driver)
    logging.info(f'Log: Start to verify size selection function')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Select a size of the product"):
        random_size = random.choice(product_page.get_all_sizes())
        product_page.click_product_size(random_size)

    with allure.step("Verify if selected size is highlighted"):
        assert 'product__size--selected' in random_size.get_attribute('class'), \
            f"The selected size isn't highlighted"
    
    logging.info('Log: End of verify size selection function')

@allure.feature('Product Page Related Feature - Quantity Editor Disabled')
def test_quantity_editor_disabled(driver):

    product_page = ProductPage(driver)
    logging.info(f'Log: Start to verify quantity editor disabled')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Get current product quantity"):
        expected = product_page.get_product_quantity()
        logging.info(f"Log: The current product quantity is: {expected}")

    with allure.step("Edit quantity without size selection"):
        product_page.edit_product_quantity('add', 2)
        result = product_page.get_product_quantity()
        logging.info(f"Log: The new product quantity is: {result}")

    with allure.step("Verify quantity editor disabled"):
        assert expected == result, \
            f"Expected: {expected}\nActual: {result}"
    
    logging.info('Log: End of verify quantity editor disabled')

@allure.feature('Product Page Related Feature - Quantity Editor - Increase Quantity')
def test_increase_quantity(driver):

    product_page = ProductPage(driver)
    logging.info(f'Log: Start to verify increase quantity')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Select a size of the product"):
        random_size = random.choice(product_page.get_all_sizes())
        product_page.click_product_size(random_size)
        original_quantity = int(product_page.get_product_quantity())
    
    with allure.step("Add 8 more quantity"):
        edit_quantity_times = 8
        product_page.edit_product_quantity('add', edit_quantity_times)
    
    with allure.step("Verify quantity should be 9"):
        expected = original_quantity + edit_quantity_times
        assert expected == int(product_page.get_product_quantity()), \
            f"Expected: {expected}\nActual: {product_page.get_product_quantity()}"

    with allure.step("Add 2 more quantity"):
        edit_quantity_times = 2
        product_page.edit_product_quantity('add', edit_quantity_times)

    with allure.step("Verify quantity still be 9"):
        assert expected == int(product_page.get_product_quantity()), \
            f"Expected: {expected}\nActual: {int(product_page.get_product_quantity())}"
    
    logging.info('Log: End of verify increase quantity')
    
@allure.feature('Product Page Related Feature - Quantity Editor - Decrease Quantity')
def test_decrease_quantity(driver):

    product_page = ProductPage(driver)
    logging.info(f'Log: Start to verify dncrease quantity')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Select a size of the product"):
        random_size = random.choice(product_page.get_all_sizes())
        product_page.click_product_size(random_size)
        original_quantity = int(product_page.get_product_quantity())
    
    with allure.step("Add 8 more quantity"):
        edit_quantity_times = 8
        product_page.edit_product_quantity('add', edit_quantity_times)

    with allure.step("Decrease 8 quantity"):
        product_page.edit_product_quantity('minus', edit_quantity_times)

    with allure.step("Verify quantity should be 1"):
        assert original_quantity == int(product_page.get_product_quantity()), \
            f"Expected: {original_quantity}\nActual: {int(product_page.get_product_quantity())}"
    
    logging.info('Log: End of verify dncrease quantity')
       
@allure.feature('Product Page Related Feature - Add To Cart - Success')
def test_add_to_cart_success(driver):
    
    product_page = ProductPage(driver)
    logging.info(f'Log: Start to verify add to cart - Success')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Select a size of the product"):
        random_size = random.choice(product_page.get_all_sizes())
        product_page.click_product_size(random_size)
        original_quantity = int(product_page.get_product_quantity())

    with allure.step("Click add to cart button"):
        product_page.click_add_to_cart_btn()

    with allure.step("Verify success message should be shown"):
        assert "已加入購物車" == product_page.get_alert_message(), \
            f"Actual: {product_page.get_alert_message()}"

    with allure.step("Verify cart icon number should be 1"):
        assert original_quantity == int(product_page.get_cart_icon_number()), \
            f"Expected: {original_quantity}\nActual: {int(product_page.get_cart_icon_number())}"
    
    logging.info(f'Log: End of verify add to cart - Success')
    
@allure.feature('Product Page Related Feature - Add To Cart - Failed')
def test_add_to_cart_failed(driver):

    product_page = ProductPage(driver)
    logging.info(f'Log: Start to verify add to cart - Failed')
    
    with allure.step("Entered a product page"):
        enter_product_page_from_category_page(driver)

    with allure.step("Click add to cart button without size selection"):
        product_page.click_add_to_cart_btn()

    with allure.step("Verify alert message should be shown"):
        assert "請選擇尺寸" == product_page.get_alert_message(), \
            f"Actual: {product_page.get_alert_message()}"
    
    logging.info(f'Log: End of verify add to cart - Failed')