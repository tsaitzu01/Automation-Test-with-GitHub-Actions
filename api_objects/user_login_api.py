import os
from utils.api_base import APIBase

class UserLoginAPI(APIBase):

    def __init__(self, session, email = '', password = ''):
        super().__init__(session)
        self.email = email
        self.password = password
        self.payload = {
            "provider": "native",
            "email": "%s" % email,
            "password": "%s" % password
        }

    def send_login(self):
        url = os.environ.get('API_DOMAIN') + '/user/login'
        self.api_request("post", url, json = self.payload)
        return self