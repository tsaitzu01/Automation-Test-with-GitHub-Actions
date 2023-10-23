import os
from utils.api_base import APIBase

class ProductSearchAPI(APIBase):

    def send_product_search(self, keyword, paging):
        url = os.environ.get('API_DOMAIN') + f'/products/search?keyword={keyword}&paging={paging}'
        self.api_request("get", url)
        return self