import pytest
import allure
import logging
import os
from page_objects.search_page import SearchPage
from .test_data.product_detail import ProductDetail

@allure.feature('Product Search Feature')
@pytest.mark.parametrize('keyword', ['洋裝', '', 'Hello'])
def test_web_search(driver, db_connection, keyword):

    driver.get(os.environ.get('DOMAIN'))
    logging.info(f'Log: Start to Search Product by keyword: {keyword}')
    search_page = SearchPage(driver)

    logging.info(f'Log: Start to input and send keyword: {keyword}')
    search_page.input_search_keyword(keyword)
    search_page.send_search_keyword()

    logging.info('Log: Start to get search results and verify')
    results = sorted([result.text for result in search_page.get_search_results()])
    expected = sorted(ProductDetail().select_products_by_keyword(db_connection, keyword))

    assert expected == results, \
        f"Expected: {expected}\nActual: {results}"
    logging.info('Log: End of Search Product Without Keyword')