from utilities.requests_utility import assert_status_code
from pathlib import Path

import requests


class RequestsClient(object):

    def __init__(self, app):
        self.app = app
        self.base_url = {
            "user": app.config['requests']['host_user'],
            "admin": app.config['requests']['host_admin']
        }
        self.auth_helper = app.auth_helper

    def create_request(self, source_name, endpoint, role):
        url = self.base_url[role] + endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_helper.get_token(role)}"
        }
        source_file = Path("../data") / source_name
        with open(source_file, "rb") as data:
            response = requests.post(url, headers=headers, data=data)
        status_code = response.status_code
        assert_status_code(status_code)
        rs_json = response.json()
        return rs_json

    def get_request_by_id(self, request_id, role):
        url = self.base_url["user"] + f"requests/{request_id}"
        headers = {
            "Authorization": f"Bearer {self.auth_helper.get_token(role)}"
        }
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        assert_status_code(status_code)
        rs_json = response.json()
        return rs_json

    def update_request_rate_by_id(self, source_name, endpoint, request_id):
        url = self.base_url["admin"] + endpoint + f"{request_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_helper.get_token('admin')}"
        }
        source_file = Path("../data") / source_name
        with open(source_file, "rb") as data:
            response = requests.patch(url, headers=headers, data=data)
        status_code = response.status_code
        assert_status_code(status_code)
        rs_json = response.json()
        return rs_json

    def change_request_status_by_id(self, request_id, status):
        url = self.base_url["admin"] + f"requests/{status}/{request_id}"
        headers = {
            "Authorization": f"Bearer {self.auth_helper.get_token('admin')}"
        }
        response = requests.post(url, headers=headers)
        status_code = response.status_code
        assert_status_code(status_code)
        rs_json = response.json()
        return rs_json
