import os

class DbQuery():

    def get_all_product_ids(db_connection):
        select_all = ("SELECT id FROM product ")

        db_connection.execute(select_all)
        results = db_connection.fetchall()
        
        return [item['id'] for item in results]

    def get_product_by_category(db_connection, category):       
        categories = {
            '女裝' : 'women',
            '男裝' : 'men',
            '配件' : 'accessories',
            '全部' : '%'
        }

        select_category = ("SELECT title FROM product "
                           f"WHERE category LIKE '{categories.get(category)}' ")

        db_connection.execute(select_category)
        results = db_connection.fetchall()

        return [item['title'] for item in results]

    def select_products_by_keyword(db_connection, keyword):
        all_products_title = ("SELECT title FROM product "
                              f"WHERE title LIKE '%{keyword}%'")

        db_connection.execute(all_products_title)
        results = db_connection.fetchall()

        return [item['title'] for item in results]
    
    def get_color_by_color_code(self, db_connection, color_code):
        select_color = ("SELECT name FROM color "
                        f"WHERE code = '{color_code}'")
        
        db_connection.execute(select_color)
        results = db_connection.fetchall()

        return results[0]['name']
    
    def get_user_profile(db_connection, email):
        select_user_profile = ("SELECT id, provider, email, name, picture, access_token, access_expired, login_at FROM user "
                               f"WHERE email = '{email}'")
        db_connection.execute(select_user_profile)
        results = db_connection.fetchall()

        return results[0]
    
    def get_product_info(db_connection, filter_column, filter_by, product_index = 0):
        if filter_column == 'category' and filter_by == 'all':
            filter_by = '%'
        elif filter_column == 'title':
            filter_by = f"%{filter_by}%"
        select_product = ("SELECT * FROM stylish_backend.product "
                          f"WHERE {filter_column} LIKE '{filter_by}'"
                          f"LIMIT 1 OFFSET {product_index}")

        db_connection.execute(select_product)
        results = db_connection.fetchall()
        
        results[0]['main_image'] = f"{os.environ.get('IMAGE_DOMAIN')}{results[0]['id']}/{results[0]['main_image']}"

        select_image = ("SELECT image FROM stylish_backend.product_images " 
                        f"WHERE product_id = '{results[0]['id']}'")
        
        select_variant = ("SELECT color.code as 'color_code', size, stock "
                          "FROM stylish_backend.variant "
                          "INNER JOIN stylish_backend.color "
                          "ON variant.color_id = color.id "
                          f"WHERE product_id = '{results[0]['id']}'")
        
        select_color = ("SELECT DISTINCT color.code, name "
                        "FROM stylish_backend.variant "
                        "INNER JOIN stylish_backend.color "
                        "ON variant.color_id = color.id "
                        f"WHERE product_id = '{results[0]['id']}'")
        
        select_distinct_size = ("SELECT DISTINCT size FROM stylish_backend.variant "
                                f"WHERE product_id = '{results[0]['id']}'")
        
        db_connection.execute(select_image)
        results[0]['images'] = [f"{os.environ.get('IMAGE_DOMAIN')}{results[0]['id']}/{item['image']}" for item in db_connection.fetchall()]
        db_connection.execute(select_variant)
        results[0]['variants'] = db_connection.fetchall()
        db_connection.execute(select_color)
        results[0]['colors'] = db_connection.fetchall()
        db_connection.execute(select_distinct_size)
        results[0]['sizes'] = [item.get('size', '') for item in db_connection.fetchall()]

        return results[0]