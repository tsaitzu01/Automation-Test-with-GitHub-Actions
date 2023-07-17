import os
from utils.api_base import APIBase

class DeleteProductAPI(APIBase):

    def send_delete_product(self, product_id):
        url = os.environ.get('API_DOMAIN') + f'/admin/product/{product_id}'
        self.api_request("delete", url)
        return self