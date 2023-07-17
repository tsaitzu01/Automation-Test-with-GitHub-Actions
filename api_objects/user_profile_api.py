import os
from utils.api_base import APIBase

class UserProfileAPI(APIBase):

    def send_profile(self):
        url = os.environ.get('API_DOMAIN') + '/user/profile'
        self.api_request("get", url)
        return self