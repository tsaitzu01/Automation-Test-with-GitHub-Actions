import os
from utils.api_base import APIBase

class UserLogoutAPI(APIBase):

    def send_logout(self):
        url = os.environ.get('API_DOMAIN') + '/user/logout'
        self.api_request("post", url)
        return self