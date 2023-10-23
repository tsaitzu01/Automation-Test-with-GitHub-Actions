import os
from utils.api_base import APIBase
import logging
import json
import urllib

class PrimeAPI(APIBase):

    def __init__(self, session, cardnumber = '', cardduedate = '', cardccv = ''):
        super().__init__(session)
        self.cardnumber = cardnumber
        self.cardduedate = cardduedate
        self.payload = json.dumps({
            "cardnumber": f"{cardnumber}",
            "cardduedate": f"{cardduedate}",
            "appid": 12348,
            "appkey": os.environ.get('APP_KEY'),
            "appname": os.environ.get('DB_HOST'),
            "url": os.environ.get('DOMAIN'),
            "port": "",
            "protocol": "http:",
            "fraudid":"",
            "cardccv": f"{cardccv}"
        })
        self.body = 'jsonString=' + urllib.parse.quote(self.payload)
        logging.info(f'Log: The request body of getting prime data is {self.payload}')

    def send_get_prime(self):
        url = "https://js.tappaysdk.com/tpdirect/sandbox/getprime"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Api-Key": os.getenv("APP_KEY"),
        }
        self.api_request("post", url, headers = headers, data=self.body)
        return self