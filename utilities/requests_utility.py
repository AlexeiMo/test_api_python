import json
import logging

import requests

LOGGER = logging.getLogger(__name__)


class RequestUtility:
    token = None

    def __init__(self, group):
        self.auth_url = group.auth_url
        self.base_url = group.base_url

    @staticmethod
    def assert_status_code(actual_status_code, expected_status_code):
        assert actual_status_code == expected_status_code, f"Bad Status code. " \
                                                           f"Expected: {expected_status_code}, " \
                                                           f"Actual: {actual_status_code}."

    def authorize(self, username, password, headers=None):
        if not headers:
            headers = {"Content-Type": "application/json"}
        payload = {
            "data": {
                "email": f"{username}",
                "password": f"{password}"
            }
        }
        response = requests.post(self.auth_url, headers=headers, data=json.dumps(payload))
        status_code = response.status_code
        rs_json = response.json()
        self.assert_status_code(status_code, 200)
        if not rs_json['data']['refreshToken']:
            raise Exception("Invalid authorization response: no token found")
        else:
            self.token = rs_json['data']['refreshToken']
        # LOGGER.debug(f"POST API response: {rs_json}")
        return rs_json

    def get(self, endpoint, data=None, headers=None, expected_status_code=200):
        if not self.token:
            raise Exception("Trying to send API request without proper authorization")
        if not headers:
            headers = {"Content-Type": "application/json"}
        headers["Authorization"] = f"Bearer {self.token}"
        url = self.base_url + endpoint
        response = requests.get(url, headers=headers, data=json.dumps(data))
        status_code = response.status_code
        rs_json = response.json()
        self.assert_status_code(status_code, expected_status_code)
        # LOGGER.debug(f"GET API response: {rs_json}")
        return rs_json
