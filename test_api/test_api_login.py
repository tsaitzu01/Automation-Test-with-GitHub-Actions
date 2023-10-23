import pytest
import allure
import os
from api_objects import UserLoginAPI, UserLogoutAPI, UserProfileAPI
from db_query import DbQuery
from datetime import datetime

@allure.feature('User APIs')
@allure.story('Login Success')
def test_login_success(db_connection, login_success):

    with allure.step("Verify response code is 200"):
        status_code = login_success.get_status_code()
        assert status_code == 200, \
            f"When login successfully, the response code of /user/login is {status_code}"
        
    with allure.step("Verify the data of response body is correct"):

        results = login_success.get_response_body()['data']
        results['login_at']  = results['login_at'][:17]
        
        user_profile = DbQuery.get_user_profile(db_connection, login_success.email)
        datetime_obj = datetime.strptime(f"{user_profile['login_at']}", "%Y-%m-%d %H:%M:%S")
        expected = {
            'access_token': f"{user_profile['access_token']}",
            'access_expired': f"{user_profile['access_expired']}",
            'login_at': f"{datetime_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:17]}",
            'user': {
                'id': user_profile['id'],
                'email': f"{user_profile['email']}",
                'name': f"{user_profile['name']}",
                'picture': user_profile['picture'],
                'provider': f"{user_profile['provider']}"
            }
        }
        assert results == expected, \
            f"Actual: {results}\nExpected: {expected}"

@allure.feature('User APIs')
@allure.story('Login Failed with incorrect email or password')
@pytest.mark.parametrize("login", [{"email": "kathyfail@gmail", "password": os.environ.get('PASSWORD')}, 
                                   {"email": os.environ.get('EMAIL'), "password": "fail"},
                                   {"email": os.environ.get('EMAIL'), "password": ""},
                                   {"email": "", "password": os.environ.get('PASSWORD')}], indirect=True)
def test_login_failed(session, login):

    with allure.step("Verify response code is 400"):
        status_code = login.get_status_code()
        assert status_code == 400, \
            f"When login failed, the response code of /user/login is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        if login.email == '' or login.password == '':
            assert login.get_response_body() == {'errorMsg': 'Email and password are required.'}, \
                f"Actual: {login.get_response_body()}\nExpected: Email and password are required."
        else:
            assert login.get_response_body() == {"errorMsg": "Login Failed"}, \
                f"Actual: {login.get_response_body()}\nExpected: Login Failed"
            
@allure.feature('User APIs')
@allure.story('Logout Success')
def test_logout_success(session, login_success):
    user_logout_api = UserLogoutAPI(session)
    
    with allure.step("Member logout"):
        user_logout_api.send_logout()

    with allure.step("Verify response code is 200"):
        status_code = user_logout_api.get_status_code()
        assert status_code == 200, \
            f"When logout successfully, the response code of /user/logout is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        assert user_logout_api.get_response_body() == {'message': 'Logout Success'}, \
            f"Actual response body: {user_logout_api.get_response_body()}"
        
@allure.feature('User APIs')
@allure.story('Logout Without Token')
def test_logout_without_token(session):
    user_logout_api = UserLogoutAPI(session)

    with allure.step("Member logout"):
        user_logout_api.send_logout()

    with allure.step("Verify response code is 401"):
        status_code = user_logout_api.get_status_code()
        assert status_code == 401, \
            f"When logout successfully, the response code of /user/logout is {status_code}"

    with allure.step("Verify the response body is correct"):
        assert user_logout_api.get_response_body() == {'errorMsg': 'Unauthorized'}, \
            f"Actual response body: {user_logout_api.get_response_body()}"
        
@allure.feature('User APIs')
@allure.story('Logout With Invalid Token')
def test_logout_with_invalid_token(session):
    user_logout_api = UserLogoutAPI(session)
    
    with allure.step("Remove access token from the Header"):
        session.headers["Authorization"] = "Invalid Token"

    with allure.step("Member logout"):
        user_logout_api.send_logout()

    with allure.step("Verify response code is 401"):
        status_code = user_logout_api.get_status_code()
        assert status_code == 403, \
            f"When logout successfully, the response code of /user/logout is {status_code}"

    with allure.step("Verify the response body is correct"):
        assert user_logout_api.get_response_body() == {'errorMsg': 'Forbidden'}, \
            f"Actual response body: {user_logout_api.get_response_body()}"
        
@allure.feature('User APIs')
@allure.story('Get User Profile Success')
def test_get_profile_success(session, db_connection, login_success):
    user_profile_api = UserProfileAPI(session)
    
    with allure.step("Get user profile"):
        user_profile_api.send_profile()

    with allure.step("Verify response code is 200"):
        status_code = user_profile_api.get_status_code()
        assert status_code == 200, \
            f"When get user profile successfully, the response code of /user/profile is {status_code}"
        
    with allure.step("Verify the response body is correct"):
        
        results = user_profile_api.get_response_body()['data']

        user_profile = DbQuery.get_user_profile(db_connection, login_success.email)
        expected = {
            'provider': f"{user_profile['provider']}",
            'email': f"{user_profile['email']}",
            'name': f"{user_profile['name']}",
            'picture': user_profile['picture']
        }
        assert results == expected, \
            f"Actual: {results}\nExpected: {expected}"
        
@allure.feature('User APIs')
@allure.story('Get User Profile Without Token')
def test_get_profile_without_token(session):
    user_profile_api = UserProfileAPI(session)

    with allure.step("Get user profile"):
        user_profile_api.send_profile()

    with allure.step("Verify response code is 401"):
        status_code = user_profile_api.get_status_code()
        assert status_code == 401, \
            f"When logout successfully, the response code of /user/logout is {status_code}"

    with allure.step("Verify the response body is correct"):
        assert user_profile_api.get_response_body() == {'errorMsg': 'Unauthorized'}, \
            f"Actual response body: {user_profile_api.get_response_body()}"
        
@allure.feature('User APIs')
@allure.story('Get User Profile With Invalid Token')
def test_get_profile_with_invalid_token(session):
    user_profile_api = UserProfileAPI(session)
    
    with allure.step("Remove access token from the Header"):
        session.headers["Authorization"] = "Invalid Token"

    with allure.step("Get user profile"):
        user_profile_api.send_profile()

    with allure.step("Verify response code is 401"):
        status_code = user_profile_api.get_status_code()
        assert status_code == 403, \
            f"When logout successfully, the response code of /user/logout is {status_code}"

    with allure.step("Verify the response body is correct"):
        assert user_profile_api.get_response_body() == {'errorMsg': 'Forbidden'}, \
            f"Actual response body: {user_profile_api.get_response_body()}"