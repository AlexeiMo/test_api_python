import requests
from utilities.requests_utility import assert_status_code


class TransactionsClient(object):

    def __init__(self, app):
        self.app = app
        self.base_url = app.config['transactions']['host']
        self.auth_helper = app.auth_helper

    def get_transaction_by_id(self, tr_id):
        endpoint = self.base_url + f"transactions/{tr_id}"
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {self.auth_helper.get_token(role='user')}"}
        response = requests.get(endpoint, headers=headers)
        status_code = response.status_code
        assert_status_code(status_code)
        rs_json = response.json()
        return rs_json
