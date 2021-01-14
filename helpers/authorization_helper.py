import requests
import json
from utilities.requests_utility import assert_status_code


class AuthorizationHelper(object):
    tokens = {"user": None,
              "admin": None}

    def __init__(self, app):
        self.app = app
        self.base_url = app.config['authorization']['host']

    def authorize(self, username, password, role):
        if self.tokens[role]:
            return self.tokens[role]
        else:
            headers = {"Content-Type": "application/json"}
            data = {
                "data": {
                    "email": f"{username}",
                    "password": f"{password}"
                }
            }
            response = requests.post(self.base_url, headers=headers, data=json.dumps(data))
            status_code = response.status_code
            assert_status_code(status_code)
            rs_json = response.json()
            if not rs_json['data']['refreshToken']:
                raise Exception("Invalid authorization response: no token found")
            else:
                self.tokens[role] = rs_json['data']['refreshToken']
            return self.tokens[role]

    def get_token(self, role):
        return self.tokens[role]
