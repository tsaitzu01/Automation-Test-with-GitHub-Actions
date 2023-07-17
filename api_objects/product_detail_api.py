import os
from utils.api_base import APIBase

class ProductDetailAPI(APIBase):

    def send_product_detail(self, product_id):
        url = os.environ.get('API_DOMAIN') + f'/products/details?id={product_id}'
        self.api_request("get", url)
        return self