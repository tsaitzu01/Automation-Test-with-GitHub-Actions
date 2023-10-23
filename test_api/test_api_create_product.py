import allure
import pytest
import logging
from test_data.get_data_from_excel import GetDataFromExcel
from api_objects import CreateProductAPI, DeleteProductAPI
from db_query import DbQuery

@allure.feature('Create Product API')
@allure.step('Create Product Success')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_create_product('API Create Product Success'))
def test_create_product_success(session, login_success, test_data, db_connection, request):

    with allure.step("Generate a new product"):
        other_images = []
        if test_data['Other Image 1'] != '':
            other_images.append(test_data['Other Image 1'])
        if test_data['Other Image 2'] != '':
            other_images.append(test_data['Other Image 2'])
        product_info = {
            'category': test_data['Category'],
            'title': test_data['Title'],
            'description': test_data['Description'],
            'price': test_data['Price'],
            'texture': test_data['Texture'],
            'wash': test_data['Wash'],
            'place': test_data['Place of Product'],
            'note': test_data['Note'],
            'color_ids': test_data['ColorIDs'],
            'sizes': test_data['Sizes'],
            'story': test_data['Story'],
            'main_image': test_data['Main Image'],
            'other_images': other_images
        }
        logging.info(f"Log: Product info is {product_info}")
    
    with allure.step("Create the new product"):
        create_product_api = CreateProductAPI(session, product_info = product_info)
        create_product_api.send_create_product()

    with allure.step("Verify response code is 200"):
        status_code = create_product_api.get_status_code()
        assert status_code == 200, \
            f"When create product successfully, the response code is {status_code}"
        
    with allure.step("Verify the response body after create product success"):
        assert create_product_api.get_response_body()['data']['product_id'] != None, \
            f"When create product successfully, the response body is {create_product_api.get_response_body()}"
        
    with allure.step("Verify the product information in the database is correct"):
        new_product_id = create_product_api.get_response_body()['data']['product_id']
        db_product_info = DbQuery.get_product_info(db_connection, 'id', new_product_id, product_index = 0)
        assert product_info['category'] == db_product_info['category']
        assert product_info['title'] == db_product_info['title']
        assert product_info['description'] == db_product_info['description']
        assert product_info['price'] == db_product_info['price']
        assert product_info['texture'] == db_product_info['texture']
        assert product_info['wash'] == db_product_info['wash']
        assert product_info['place'] == db_product_info['place']
        assert product_info['note'] == db_product_info['note']
        assert product_info['sizes'] == db_product_info['sizes']
        assert product_info['story'] == db_product_info['story']
        assert product_info['main_image'] == db_product_info['main_image'].split('/')[-1]
        assert product_info['other_images'] == [item.split('/')[-1] for item in db_product_info['images']]
        
    def finalizer():
        with allure.step("Reset the data in a database: delete product"):
            delete_product_api = DeleteProductAPI(session)
            delete_product_api.send_delete_product(new_product_id)
            
            status_code = delete_product_api.get_status_code()
            assert status_code == 200, \
                f"When delete product successfully, the response code is {status_code}"
        
    request.addfinalizer(finalizer)

@allure.feature('Create Product API')
@allure.step('Create Product Failed')
@pytest.mark.parametrize('test_data', GetDataFromExcel.read_create_product('API Create Product Failed'))
def test_create_product_failed(session, login_success, test_data, db_connection, request):

    with allure.step("Generate a new product"):
        other_images = []
        if test_data['Other Image 1'] != '':
            other_images.append(test_data['Other Image 1'])
        if test_data['Other Image 2'] != '':
            other_images.append(test_data['Other Image 2'])
        product_info = {
            'category': test_data['Category'],
            'title': test_data['Title'],
            'description': test_data['Description'],
            'price': test_data['Price'],
            'texture': test_data['Texture'],
            'wash': test_data['Wash'],
            'place': test_data['Place of Product'],
            'note': test_data['Note'],
            'color_ids': test_data['ColorIDs'],
            'sizes': test_data['Sizes'],
            'story': test_data['Story'],
            'main_image': test_data['Main Image'],
            'other_images': other_images
        }
        logging.info(f"Log: Product info is {product_info}")
    
    with allure.step("Create the new product"):
        create_product_api = CreateProductAPI(session, product_info = product_info)
        create_product_api.send_create_product()

    with allure.step("Verify response code is 400"):
        status_code = create_product_api.get_status_code()
        assert status_code == 400, \
            f"When create product successfully, the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert create_product_api.get_response_body()['errorMsg'] == test_data['Error Msg'], \
            f"Actual response body: {create_product_api.get_response_body()}"
        
    def finalizer():
        with allure.step("Reset the data in a database: delete product"):
            all_product_titles = DbQuery.get_all_product_titles(db_connection)
            if product_info['title'] in all_product_titles:
                new_product_id = create_product_api.get_response_body()['data']['product_id']
                delete_product_api = DeleteProductAPI(session)
                delete_product_api.send_delete_product(new_product_id)
            
                status_code = delete_product_api.get_status_code()
                assert status_code == 200, \
                    f"When delete product successfully, the response code is {status_code}"
                
    request.addfinalizer(finalizer)

@allure.feature('Create Product API')
@allure.step('Create Product Without Login')
def test_create_product_without_login(session, db_connection, request):
    
    with allure.step("Create the new product without login"):
        product_info = {
            'category': 'men',
            'title': 'Without_Login',
            'description': 'x',
            'price': 100,
            'texture': 'x',
            'wash': 'x',
            'place': 'x',
            'note': 'x',
            'color_ids': ['2', '3'],
            'sizes': ['L', 'XL'],
            'story': 'x',
            'main_image': 'mainImage.jpg',
            'other_images': ['otherImage0.jpg', 'otherImage1.jpg']
        }
        create_product_api = CreateProductAPI(session, product_info = product_info)
        create_product_api.send_create_product()

    with allure.step("Verify response code is 401"):
        status_code = create_product_api.get_status_code()
        assert status_code == 401, \
            f"When create product without login, the response code is {status_code}"
    
    with allure.step("Verify the response body is correct"):
        assert create_product_api.get_response_body() == {'errorMsg': 'Unauthorized'}, \
            f"Actual response body: {create_product_api.get_response_body()}"
        
    def finalizer():
        with allure.step("Reset the data in a database: delete product"):
            all_product_titles = DbQuery.get_all_product_titles(db_connection)
            if product_info['title'] in all_product_titles:
                new_product_id = create_product_api.get_response_body()['data']['product_id']
                delete_product_api = DeleteProductAPI(session)
                delete_product_api.send_delete_product(new_product_id)
            
                status_code = delete_product_api.get_status_code()
                assert status_code == 200, \
                    f"When delete product successfully, the response code is {status_code}"
                
    request.addfinalizer(finalizer)

@allure.feature('Delete Product API')
@allure.step('Delete Product Without Login')
def test_delete_product_without_login(session):

    with allure.step("Delete product without login"):
            delete_product_api = DeleteProductAPI(session)
            delete_product_api.send_delete_product('201807242228')
            
    with allure.step("Verify response code is 401"):
        status_code = delete_product_api.get_status_code()
        assert status_code == 401, \
            f"When delete product without login, the response code is {status_code}"
    
    with allure.step("Verify the response body is correct"):
        assert delete_product_api.get_response_body() == {'errorMsg': 'Unauthorized'}, \
            f"Actual response body: {delete_product_api.get_response_body()}"

@allure.feature('Delete Product API')
@allure.step('Delete Product Without Given Product ID')
def test_delete_product_without_id(session, login_success):

    with allure.step("Delete product with invalid product id"):
            delete_product_api = DeleteProductAPI(session)
            delete_product_api.send_delete_product('')    

    with allure.step("Verify response code is 404"):
        status_code = delete_product_api.get_status_code()
        assert status_code == 404, \
            f"When delete product without given id, the response code is {status_code}"      

@allure.feature('Delete Product API')
@allure.step('Delete Product With Invalid Product ID')
@pytest.mark.parametrize('product_id', [0, '123', ' ', ' 123'])
def test_delete_product_with_invalid_id(session, login_success, product_id):

    with allure.step("Delete product with invalid product id"):
            delete_product_api = DeleteProductAPI(session)
            delete_product_api.send_delete_product(product_id)    

    with allure.step("Verify response code is 401"):
        status_code = delete_product_api.get_status_code()
        assert status_code == 400, \
            f"When delete product id '{product_id}', the response code is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert delete_product_api.get_response_body() == {'errorMsg': 'Product ID not found.'}, \
            f"Actual response body: {delete_product_api.get_response_body()}"