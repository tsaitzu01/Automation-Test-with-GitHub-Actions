import pytest
import allure
import logging
from page_objects.category_page import CategoryPage

logger = logging.getLogger()

@allure.feature('check products in category should be display')
@pytest.mark.parametrize('category', ['女裝', '男裝', '配件'])
def test_web_category(driver, category):
    driver.get('http://54.201.140.239/')
    logger.info('Log: Start to test web category')

    expected_product_lists = {
        '女裝' : ['前開衩扭結洋裝', '透肌澎澎防曬襯衫', '小扇紋細織上衣', '活力花紋長筒牛仔褲', '精緻扭結洋裝', '透肌澎澎薄紗襯衫', '小扇紋質感上衣', '經典修身長筒牛仔褲'],
        '男裝' : ['純色輕薄百搭襯衫', '時尚輕鬆休閒西裝', '經典商務西裝'],
        '配件' : ['夏日海灘戶外遮陽帽', '經典牛仔帽', '卡哇伊多功能隨身包', '柔軟氣質羊毛圍巾']
    }

    category_page = CategoryPage(driver)

    logger.info('Log: Start to click header category')
    category_page.click_header_category(category)
    logger.info('Log: Start to get product list')
    category_products_elem = [product.text for product in category_page.get_product_list()]
    
    assert category_products_elem == expected_product_lists.get(category), \
        f"Expected: {expected_product_lists.get(category)}, Actual: {category_products_elem}" 
    logger.info('Log: Web category test is end')