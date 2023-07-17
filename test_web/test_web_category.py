import pytest
import allure
import logging
import os
from page_objects import CategoryPage
from .test_data.product_detail import ProductDetail

@allure.feature('Category Selection')
@pytest.mark.parametrize('category', ['女裝', '男裝', '配件'])
def test_web_category(driver, db_connection, category):

    driver.get(os.environ.get('DOMAIN'))
    logging.info('Log: Start to Category Selection')
    category_page = CategoryPage(driver)

    logging.info(f'Log: Start to select category: {category}')
    category_page.click_header_category(category)
    
    logging.info('Log: Start to get product list and verify')
    results = [product.text for product in category_page.get_product_list()]
    expected = ProductDetail().get_product_by_category(db_connection, category)
    
    assert expected == results, \
        f"Expected: {expected}, Actual: {results}" 
    logging.info('Log: End of Category Selection')