import json

class APIBase():

    def __init__(self, session):
        self.response = None
        self.session = session

    def api_request(self, method, url, **kwargs):
        self.response = self.session.request(method, url, **kwargs)

    def get_status_code(self):
        return self.response.status_code
    
    def get_response_body(self):
        return self.response.json()
    
    def get_request_body(self):
        return json.loads(self.response.request.body.decode('utf-8'))