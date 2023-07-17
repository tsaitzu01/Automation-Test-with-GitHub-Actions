class ProductDetail():

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

        return [item for item, in results]

    def select_products_by_keyword(self, db_connection, keyword):
        all_products_title = ("SELECT title FROM product "
                              f"WHERE title LIKE '%{keyword}%'")

        db_connection.execute(all_products_title)
        results = db_connection.fetchall()

        return [item for item, in results]