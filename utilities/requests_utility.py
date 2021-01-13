import json
import logging

import requests

LOGGER = logging.getLogger(__name__)


class RequestUtility(object):
    tokens = {
        "user": None,
        "admin": None
    }

    def authorize(self, endpoint, username, password, role, headers=None):
        if not self.tokens[role]:
            if not headers:
                headers = {"Content-Type": "application/json"}
            payload = {
                "data": {
                    "email": f"{username}",
                    "password": f"{password}"
                }
            }
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            status_code = response.status_code
            rs_json = response.json()
            self.assert_status_code(status_code, 200)
            if not rs_json['data']['refreshToken']:
                raise Exception("Invalid authorization response: no token found")
            else:
                self.tokens[role] = rs_json['data']['refreshToken']
            return rs_json

    def get(self, endpoint, data=None, headers=None, role="user", expected_status_code=200):
        self.check_token(role)
        if not headers:
            headers = {"Content-Type": "application/json"}
        headers["Authorization"] = f"Bearer {self.tokens[role]}"
        response = requests.get(endpoint, headers=headers, data=data)
        status_code = response.status_code
        rs_json = response.json()
        self.assert_status_code(status_code, expected_status_code)
        return rs_json

    def post(self, endpoint, headers=None, data=None, files=None, role="user", expected_status_code=200):
        self.check_token(role)
        if not headers:
            headers = dict()
        headers["Authorization"] = f"Bearer {self.tokens[role]}"
        response = requests.post(endpoint, headers=headers, data=data, files=files)
        status_code = response.status_code
        rs_json = response.json()
        self.assert_status_code(status_code, expected_status_code)
        return rs_json

    def patch(self, endpoint, headers=None, data=None, role="user", expected_status_code=200):
        self.check_token(role)
        if not headers:
            headers = dict()
        headers["Authorization"] = f"Bearer {self.tokens[role]}"
        response = requests.patch(endpoint, headers=headers, data=data)
        status_code = response.status_code
        rs_json = response.json()
        self.assert_status_code(status_code, expected_status_code)
        return rs_json

    def delete(self, endpoint, headers=None, role="user", expected_status_code=200):
        self.check_token(role)
        if not headers:
            headers = dict()
        headers["Authorization"] = f"Bearer {self.tokens[role]}"
        response = requests.delete(endpoint, headers=headers)
        status_code = response.status_code
        self.assert_status_code(status_code, expected_status_code)

    def check_token(self, role="user"):
        if not self.tokens[role]:
            raise Exception("Trying to send API request without proper authorization")

    @staticmethod
    def assert_status_code(actual_status_code, expected_status_code):
        assert actual_status_code == expected_status_code, f"Bad Status code. " \
                                                           f"Expected: {expected_status_code}, " \
                                                           f"Actual: {actual_status_code}."
