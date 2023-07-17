import os
from utils.api_base import APIBase

class CreateProductAPI(APIBase):

    def __init__(self, session, product_info = ''):
        super().__init__(session)
        self.payload = product_info
        self.files = []
        if product_info['main_image'] != "":
            main_image = f"./test_data/{product_info['main_image']}"
            self.files.append(('main_image', open(main_image, 'rb')))

        for image in product_info['other_images']:
            image_path = f"./test_data/{image}"
            self.files.append(('other_images', open(image_path, 'rb')))

    def send_create_product(self):
        url = os.environ.get('API_DOMAIN') + '/admin/product'
        self.api_request("post", url, data=self.payload, files=self.files)
        return self