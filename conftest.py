import pytest
import os
import pymysql
import pymysql.cursors

# @pytest.fixture(scope = 'module')
@pytest.fixture()
def db_connection():

    cnx = pymysql.connect(
        user = os.environ.get('DB_USERNAME'), 
        password = os.environ.get('DB_PASSWORD'),
        host = os.environ.get('DB_HOST'),
        port = int(os.environ.get('DB_PORT')),
        database = os.environ.get('DB_DATABASE')
    )
    cursor = cnx.cursor(pymysql.cursors.DictCursor)

    yield cursor

    cursor.close()
    cnx.close()