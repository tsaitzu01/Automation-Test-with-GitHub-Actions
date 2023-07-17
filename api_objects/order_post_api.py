import os
from utils.api_base import APIBase

class OrderPostAPI(APIBase):

    def __init__(self, session, prime = '', order = ''):
        super().__init__(session)
        self.prime = prime
        self.order = order
        self.payload = {
            "prime": self.prime,
            "order": self.order
        }

    def send_post_order(self):
        url = os.environ.get('API_DOMAIN') + '/order'
        self.api_request("post", url, json = self.payload)
        return self