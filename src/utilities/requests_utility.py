import json
import logging

import requests

from src.configs.hosts_config import API_HOSTS
from src.utilities.credentials_utility import CredentialsUtility

LOGGER = logging.getLogger(__name__)


class RequestUtility():

    def __init__(self):
        creds = CredentialsUtility.get_api_keys()
        self.auth_url = API_HOSTS['auth_url']
        self.base_url = API_HOSTS['base_url']
        self.accessToken = None
        self.email = creds['email']
        self.password = creds['password']
        self.token = None
        self.login()

    def assert_status_code(self, actual_status_code, expected_status_code):
        assert actual_status_code == expected_status_code, f"Bad Status code. " \
                                                           f"Expected: {expected_status_code}, " \
                                                           f"Actual: {actual_status_code}."

    def login(self, headers=None):
        if not headers:
            headers = {"Content-Type": "application/json"}
        payload = {
            "data": {
                "email": f"{self.email}",
                "password": f"{self.password}"
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
