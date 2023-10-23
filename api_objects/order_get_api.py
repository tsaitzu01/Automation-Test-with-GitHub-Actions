import os
from utils.api_base import APIBase

class OrderGetAPI(APIBase):

    def send_get_order(self, order_id):
        url = os.environ.get('API_DOMAIN') + f'/order/{order_id}'
        self.api_request("get", url)
        return self