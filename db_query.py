class DbQuery():

    def get_product_by_category(self, db_connection, category):       
        categories = {
            '女裝' : 'women',
            '男裝' : 'men',
            '配件' : 'accessories'
        }

        select_category = ("SELECT title FROM product "
                           f"WHERE category = '{categories.get(category)}' ")

        db_connection.execute(select_category)
        results = db_connection.fetchall()

        return [item['title'] for item in results]

    def select_products_by_keyword(self, db_connection, keyword):
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