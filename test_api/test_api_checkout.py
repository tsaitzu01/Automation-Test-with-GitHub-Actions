import allure
import pytest
import random
import logging
from db_query import DbQuery
from api_objects import PrimeAPI, OrderPostAPI, OrderGetAPI
from test_data.get_data_from_excel import GetDataFromExcel

@allure.feature('Order APIs')
@allure.story('Checkout Success')
@pytest.mark.parametrize('time', ['anytime', 'morning', 'afternoon'])
def test_checkout_success(session, login_success, db_connection, time):

    all_products = DbQuery.get_all_product_ids(db_connection)
    random_product_id = random.choice(all_products)
    random_order_info = DbQuery.get_random_order(db_connection, [random_product_id])

    with allure.step("Generate a random order"):
        order_info = {
            "shipping": "delivery",
            "payment": "credit_card",
            "subtotal": random_order_info['subtotal'],
            "freight": 30,
            "total": random_order_info['subtotal'] + 30,
            "recipient": {
                "name": "Chan Tai Man",
                "phone": "0912345678",
                "email": "abc@abc.com",
                "address": "台北市中山區 xxxxx",
                "time": f"{time}"
            },
            "list": random_order_info['results']
        }
        logging.info(f"Log: Order info is {order_info}")
        
    with allure.step("Get Prime"):
        prime_api = PrimeAPI(session, cardnumber = '4242424242424242', cardduedate = '206912', cardccv = '123')
        prime_api.send_get_prime()
        logging.info(f"Log: Prime API response is {prime_api.get_response_body()}")
        prime_token = prime_api.get_response_body()['card']['prime']

    with allure.step("Checkout the order"):
        order_post_api = OrderPostAPI(session, prime = prime_token, order = order_info)
        order_post_api.send_post_order()
        logging.info(f"Log: Request body is {order_post_api.get_request_body()}")

    with allure.step("Verify response code is 200"):
        status_code = order_post_api.get_status_code()
        assert status_code == 200, \
            f"When checkout successfully, the response code is {status_code}"
            
    with allure.step("Verify the response body after checkout success"):
        assert order_post_api.get_response_body()['data']['number'] != None, \
            f"When checkout successfully, the response body is {order_post_api.get_response_body()}"
        logging.info(f"Log: Response body is {order_post_api.get_response_body()}")

@allure.feature('Order APIs')
@allure.story('Checkout With Invalid Value')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_checkout_value('API Checkout with Invalid Value'))
def test_checkout_with_invalid_value(session, login_success, db_connection, test_data):

    all_products = DbQuery.get_all_product_ids(db_connection)
    random_product_list = []
    for i in range(test_data['list']):
        random_product_id = random.choice(all_products)
        random_product_list.append(random_product_id)
    random_order_info = DbQuery.get_random_order(db_connection, random_product_list)

    def caculate_subtotal(price):
        if price == 1:
            return ''
        elif price == '':
            return random_order_info['subtotal']
        else:
            return price
    
    def caculate_total(price):
        if caculate_subtotal(test_data['Subtotal']) == '':
            return 0 + test_data['Freight']
        elif test_data['Freight'] == '':
            return caculate_subtotal(test_data['Subtotal']) + 0
        elif price == 1:
            return ''
        elif price == '':
            return int(caculate_subtotal(test_data['Subtotal'])) + int(test_data['Freight'])
        else:
            return price

    with allure.step("Generate a random order"):
        order_info = {
            "shipping": "delivery",
            "payment": "credit_card",
            "subtotal": caculate_subtotal(test_data['Subtotal']),
            "freight": test_data['Freight'],
            "total": caculate_total(test_data['Total']),
            "recipient": {
                "name": test_data['Receiver'],
                "phone": test_data['Mobile'],
                "email": test_data['Email'],
                "address": test_data['Address'],
                "time": test_data['Deliver Time']
            },
            "list": random_order_info['results']
        }
        logging.info(f"Log: Order info is {order_info}")

    with allure.step("Get Prime"):
        prime_api = PrimeAPI(session, cardnumber = '4242424242424242', cardduedate = '206912', cardccv = '123')
        prime_api.send_get_prime()
        logging.info(f"Log: Prime API response is {prime_api.get_response_body()}")
        prime_token = prime_api.get_response_body()['card']['prime']

    with allure.step("Checkout the order"):
        order_post_api = OrderPostAPI(session, prime = prime_token, order = order_info)
        order_post_api.send_post_order()
        logging.info(f"Log: Request body is {order_post_api.get_request_body()}")

    with allure.step("Verify response code is 400"):
        status_code = order_post_api.get_status_code()
        assert status_code == 400, \
            f"When checkout with invalid value, the response code is {status_code}"
        logging.info(f"The response body is {order_post_api.get_response_body()}")

    with allure.step("Verify the response body is correct"):
        assert order_post_api.get_response_body()['errorMsg'] == test_data['Error Msg'], \
            f"Actual response body: {order_post_api.get_response_body()}"
        
@allure.feature('Order APIs')
@allure.story('Get Order Detail By ID')
def test_get_order_success(session, login_success, db_connection):
    order_get_api = OrderGetAPI(session)

    all_orders = DbQuery.get_all_order_ids(db_connection)
    random_order_id = random.choice(all_orders)['number']

    with allure.step("Get order detail by ID"):
        order_get_api.send_get_order(random_order_id)

    with allure.step("Verify response code is 200"):
        status_code = order_get_api.get_status_code()
        assert status_code == 200, \
            f"When get order {random_order_id} successfully, the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        expected = DbQuery.get_order_info(db_connection, random_order_id)
        assert order_get_api.get_response_body()['data'] == expected, \
            f"Actual: {order_get_api.get_response_body()['data']}, Expected: {expected}"
        
@allure.feature('Order APIs')
@allure.story('Get Order Detail Without Login')
def test_get_order_without_login(session, db_connection):
    order_get_api = OrderGetAPI(session)

    all_orders = DbQuery.get_all_order_ids(db_connection)
    random_order_id = random.choice(all_orders)['number']

    with allure.step("Get order detail by ID"):
        order_get_api.send_get_order(random_order_id)

    with allure.step("Verify response code is 401"):
        status_code = order_get_api.get_status_code()
        assert status_code == 401, \
            f"When get order {random_order_id} without login, the response code is {status_code}"
    
    with allure.step("Verify the response body is correct"):
        assert order_get_api.get_response_body() == {'errorMsg': 'Unauthorized'}, \
            f"Actual response body: {order_get_api.get_response_body()}"
        
@allure.feature('Order APIs')
@allure.story('Get Order Detail Without Given ID')
def test_get_order_without_order_id(session, login_success):
    order_get_api = OrderGetAPI(session)

    with allure.step("Get order detail without given ID"):
        order_get_api.send_get_order('')

    with allure.step("Verify response code is 404"):
        status_code = order_get_api.get_status_code()
        assert status_code == 404, \
            f"When get order without given order_id, the response code is {status_code}"

@allure.feature('Order APIs')
@allure.story('Get Order Detail With Invalid ID')
@pytest.mark.parametrize('order_id', [0, '123', ' ', ' 123'])
def test_get_order_without_order_id(session, login_success, order_id):
    order_get_api = OrderGetAPI(session)

    with allure.step("Get order detail without ID"):
        order_get_api.send_get_order(order_id)

    with allure.step("Verify response code is 400"):
        status_code = order_get_api.get_status_code()
        assert status_code == 400, \
            f"When get order '{order_id}', the response code is {status_code}"
    
    with allure.step("Verify the response body is correct"):
        assert order_get_api.get_response_body() == {'errorMsg': 'Order Not Found.'}, \
            f"Actual response body: {order_get_api.get_response_body()}"