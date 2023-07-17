import os
from utils.api_base import APIBase

class ProductCategoryAPI(APIBase):

    def send_product_category(self, category, paging):
        url = os.environ.get('API_DOMAIN') + f'/products/{category}?paging={paging}'
        self.api_request("get", url)
        return self