import pytest
import allure
import logging
import math
import random
from api_objects import ProductCategoryAPI, ProductSearchAPI, ProductDetailAPI
from db_query import DbQuery

# Category
@allure.feature('Product APIs: Category')
@allure.story('Get Product By Category Success')
@pytest.mark.parametrize('category', [('all', '全部'), ('men', '男裝'), ('women', '女裝'), ('accessories', '配件')])
def test_get_product_by_category(session, db_connection, category):
    product_category_api = ProductCategoryAPI(session)

    max_num_of_each_page = 6
    total_products = len(list(DbQuery.get_product_by_category(db_connection, category[1])))
    total_page = math.ceil(total_products/max_num_of_each_page)

    for page in range(total_page):
        with allure.step(f"Get products in page {page} of {category[0]}"):
            logging.info(f"Get products in page {page} of {category[0]}")
            product_category_api.send_product_category(category[0], page)

        with allure.step("Verify response code is 200"):
            status_code = product_category_api.get_status_code()
            assert status_code == 200, \
                f"When get product successfully, the response code is {status_code}"

        with allure.step(f"Verify the maximum results of page {page} is {max_num_of_each_page}"):
            results = product_category_api.get_response_body()
            if page != total_page - 1:
                assert len(results['data']) == max_num_of_each_page, \
                    f"Actual: There are {len(results['data'])} products in this page\nExpected: There should be {max_num_of_each_page} products in this page"
            else:
                assert len(results['data']) <= max_num_of_each_page, \
                    f"Actual: There are {len(results['data'])} products in this page\nExpected: There should be <= {max_num_of_each_page} products in this page"
                
        with allure.step(f"Verify the response body of the first product in page {page}"):
            first_product = results['data'][0]
            expected = DbQuery.get_product_info(db_connection, 'category', category[0], page * max_num_of_each_page)
            assert first_product == expected, \
                f"Actual: {first_product}, Expected: {expected}"

        with allure.step("Verify there is next page and the page number is correct"):  
            if page != total_page - 1:
                assert results['next_paging'] == page + 1
            else:
                assert list(results.keys()) == ['data']

@allure.feature('Product APIs: Category')
@allure.story('Get Product Without Given Category')
def test_get_product_without_category(session):
    product_category_api = ProductCategoryAPI(session)

    with allure.step("Get products without given category"):
        product_category_api.send_product_category(category='', paging=0)
    
    with allure.step("Verify response code is 404"):
        status_code = product_category_api.get_status_code()
        assert status_code == 404, \
            f"When get product without given category, the response code is {status_code}"
        
@allure.feature('Product APIs: Category')
@allure.story('Get Product With Invalid Category')
@pytest.mark.parametrize('category', ['ALL', ' all', '.', '\''])
def test_get_product_with_invalid_category(session, category):
    product_category_api = ProductCategoryAPI(session)

    with allure.step("Get products with invalid category"):
        product_category_api.send_product_category(category, paging=0)

    with allure.step("Verify response code is 400"):
        status_code = product_category_api.get_status_code()
        assert status_code == 400, \
            f"When get product with category='{category}', the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert product_category_api.get_response_body() == {'errorMsg': 'Invalid Category'}, \
            f"Actual response body: {product_category_api.get_response_body()}"

@allure.feature('Product APIs: Category')
@allure.story('Get Product With Invalid Pagination')
@pytest.mark.parametrize(('category', 'paging'), [(('all', '全部'), '"123"'), 
                                                  (('men', '男裝'), ' '),
                                                  (('women', '女裝'), ''),
                                                  (('accessories', '配件'), 'a')])
def test_get_product_with_invalid_paging(session, db_connection, category, paging):
    product_category_api = ProductCategoryAPI(session)

    with allure.step("Get products without given category"):
        product_category_api.send_product_category(category[0], paging)
    
    with allure.step("Verify response code is 200"):
        status_code = product_category_api.get_status_code()
        assert status_code == 200, \
            f"When get products of {category[0]} with invalid pagination {paging}, the response code is {status_code}"
    
    with allure.step(f"Verify the response body of the first product in page 0"):
            first_product = product_category_api.get_response_body()['data'][0]
            expected = DbQuery.get_product_info(db_connection, 'category', category[0], 0)
            assert first_product == expected, \
                f"Actual: {first_product}, Expected: {expected}"

@allure.feature('Product APIs: Category')
@allure.story('Get Product With Out of Range Pagination')
@pytest.mark.parametrize('category', [('all', '全部'), ('men', '男裝'), ('women', '女裝'), ('accessories', '配件')])
def test_get_product_with_out_of_range_paging(session, db_connection, category):
    product_category_api = ProductCategoryAPI(session)

    max_num_of_each_page = 6
    total_products = len(list(DbQuery.get_product_by_category(db_connection, category[1])))
    total_page = math.ceil(total_products/max_num_of_each_page)

    with allure.step("Get products with out of range pagination"):
        product_category_api.send_product_category(category[0], total_page + 1)

    with allure.step("Verify response code is 200"):
        status_code = product_category_api.get_status_code()
        assert status_code == 200, \
            f"When get products in page {total_page + 1} of '{category[0]}', the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert product_category_api.get_response_body() == {'data': []}, \
            f"When get products in page {total_page + 1} of '{category[0]}', the response body {product_category_api.get_response_body()}"
        
# Search
@allure.feature('Product APIs: Search')
@allure.story('Get Product By Search Success')
@pytest.mark.parametrize('keyword', ['洋裝', '%', 'Hello'])
def test_get_product_by_search(session, db_connection, keyword):
    product_search_api = ProductSearchAPI(session)

    max_num_of_each_page = 6
    total_products = len(list(DbQuery.select_products_by_keyword(db_connection, keyword)))
    total_page = math.ceil(total_products/max_num_of_each_page)

    for page in range(total_page):
        with allure.step(f"Get products in page {page} of {keyword}"):
            logging.info(f"Get products in page {page} of {keyword}")
            product_search_api.send_product_search(keyword, page)

        with allure.step("Verify response code is 200"):
            status_code = product_search_api.get_status_code()
            assert status_code == 200, \
                f"When get products in page {total_page} of keyword '{keyword}', the response code is {status_code}"

        with allure.step(f"Verify the maximum results of page {page} is {max_num_of_each_page}"):
            results = product_search_api.get_response_body()
            if page != total_page - 1:
                assert len(results['data']) == max_num_of_each_page, \
                    f"Actual: There are {len(results['data'])} products in this page\nExpected: There should be {max_num_of_each_page} products in this page"
            else:
                assert len(results['data']) <= max_num_of_each_page, \
                    f"Actual: There are {len(results['data'])} products in this page\nExpected: There should be <= {max_num_of_each_page} products in this page"
                
        with allure.step(f"Verify the response body of the first product in page {page}"):
            first_product = results['data'][0]
            expected = DbQuery.get_product_info(db_connection, 'title', keyword, page * max_num_of_each_page)
            assert first_product == expected, \
                f"Actual: {first_product}, Expected: {expected}"

        with allure.step("Verify there is next page and the page number is correct"):  
            if page != total_page - 1:
                assert results['next_paging'] == page + 1
            else:
                assert list(results.keys()) == ['data']

@allure.feature('Product APIs: Search')
@allure.story('Get Product Without Given Keyword')
def test_get_product_without_keyword(session):
    product_search_api = ProductSearchAPI(session)

    with allure.step("Get products without given keyword"):
        product_search_api.send_product_search(keyword='', paging=0)
    
    with allure.step("Verify response code is 404"):
        status_code = product_search_api.get_status_code()
        assert status_code == 400, \
            f"When get product without given keyword, the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert product_search_api.get_response_body() == {'errorMsg': 'Search Keyword is required.'}, \
            f"Actual response body: {product_search_api.get_response_body()}"

@allure.feature('Product APIs: Search')
@allure.story('Get Product With Invalid Pagination')
@pytest.mark.parametrize(('keyword', 'paging'), [('洋裝', '"123"'), ('洋裝', ' '), ('洋裝', ''),('洋裝', 'a')])
def test_search_product_with_invalid_paging(session, db_connection, keyword, paging):
    product_search_api = ProductSearchAPI(session)

    with allure.step("Get products without given category"):
        product_search_api.send_product_search(keyword, paging)
    
    with allure.step("Verify response code is 200"):
        status_code = product_search_api.get_status_code()
        assert status_code == 200, \
            f"When get products with keyword '{keyword}' and invalid pagination {paging}, the response code is {status_code}"
    
    with allure.step(f"Verify the response body of the first product in page 0"):
            first_product = product_search_api.get_response_body()['data'][0]
            expected = DbQuery.get_product_info(db_connection, 'title', keyword, 0)
            assert first_product == expected, \
                f"Actual: {first_product}, Expected: {expected}"

@allure.feature('Product APIs: Search')
@allure.story('Get Product With Out of Range Pagination')
def test_search_product_with_out_of_range_paging(session, db_connection, keyword = '洋裝'):
    product_search_api = ProductSearchAPI(session)

    max_num_of_each_page = 6
    total_products = len(list(DbQuery.get_product_by_category(db_connection, keyword)))
    total_page = math.ceil(total_products/max_num_of_each_page)

    with allure.step("Get products with out of range pagination"):
        product_search_api.send_product_search(keyword, total_page + 1)

    with allure.step("Verify response code is 200"):
        status_code = product_search_api.get_status_code()
        assert status_code == 200, \
            f"When get products in page {total_page + 1} of '{keyword}', the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert product_search_api.get_response_body() == {'data': []}, \
            f"When get products in page {total_page + 1} of '{keyword}', the response body {product_search_api.get_response_body()}"
        
# Detail
@allure.feature('Product APIs: Detail')
@allure.story('Get Product By Product Id Success')
def test_get_product_by_id(session, db_connection):
    product_detail_api = ProductDetailAPI(session)

    all_products = DbQuery.get_all_product_ids(db_connection)
    random_product_id = random.choice(all_products)

    with allure.step(f"Get products with product_id: {random_product_id}"):
        logging.info(f"Get products with product_id: {random_product_id}")
        product_detail_api.send_product_detail(random_product_id)

    with allure.step("Verify response code is 200"):
        status_code = product_detail_api.get_status_code()
        assert status_code == 200, \
            f"When get product by product id '{random_product_id}', the response code is {status_code}"

    with allure.step(f"Verify the response body of product id '{random_product_id}'"):
        random_product = product_detail_api.get_response_body()['data']
        expected = DbQuery.get_product_info(db_connection, 'id', random_product_id)
        assert random_product == expected, \
            f"Actual: {random_product}, Expected: {expected}"
            
@allure.feature('Product APIs: Detail')
@allure.story('Get Product Without Given Product Id')
def test_get_product_without_id(session):
    product_detail_api = ProductDetailAPI(session)

    with allure.step("Get products without given product_id"):
        product_detail_api.send_product_detail('')
    
    with allure.step("Verify response code is 404"):
        status_code = product_detail_api.get_status_code()
        assert status_code == 400, \
            f"When get product without given product_id, the response code is {status_code}"
    
    with allure.step("Verify the response body is correct"):
        assert product_detail_api.get_response_body() == {'errorMsg': 'Invalid Product ID'}, \
            f"Actual response body: {product_detail_api.get_response_body()}"
        
@allure.feature('Product APIs: Detail')
@allure.story('Get Product With Invalid Product Id')
@pytest.mark.parametrize('product_id', ['"0"', ' 12', '.', '\'', 0])
def test_get_product_with_invalid_id(session, product_id):
    product_detail_api = ProductDetailAPI(session)

    with allure.step(f"Get products with invalid product_id '{product_id}'"):
        product_detail_api.send_product_detail(product_id)

    with allure.step("Verify response code is 400"):
        status_code = product_detail_api.get_status_code()
        assert status_code == 400, \
            f"When get product with category='{product_id}', the response code is {status_code}"

    with allure.step("Verify the response body is correct"):
        assert product_detail_api.get_response_body() == {'errorMsg': 'Invalid Product ID'}, \
            f"Actual response body: {product_detail_api.get_response_body()}"