from pathlib import Path

import requests
from utilities.requests_utility import assert_status_code


class FilesClient(object):

    def __init__(self, app):
        self.app = app
        self.base_url = app.config["files"]["host"]
        self.auth_helper = app.auth_helper

    def upload_file_from_user(self, filename, content_type, user_id):
        endpoint = self.base_url + f"files/private/{user_id}"
        headers = {"Authorization": f"Bearer {self.auth_helper.get_token(role='user')}"}
        file_to_open = Path("../data") / filename
        with open(file_to_open, "rb") as file:
            files = {"file": (filename, file, content_type)}
            response = requests.post(endpoint, headers=headers, files=files)
        status_code = response.status_code
        assert_status_code(status_code)
        rs_json = response.json()
        return rs_json

    def delete_file_by_id(self, file_id):
        endpoint = self.base_url + f"files/{file_id}"
        headers = {"Authorization": f"Bearer {self.auth_helper.get_token(role='user')}"}
        response = requests.delete(endpoint, headers=headers)
        status_code = response.status_code
        assert_status_code(status_code)

    def get_all_files_of_user(self, user_id):
        endpoint = self.base_url + f"users/{user_id}"
        headers = {"Authorization": f"Bearer {self.auth_helper.get_token(role='user')}"}
        response = requests.get(endpoint, headers=headers)
        status_code = response.status_code
        assert_status_code(status_code, 200)
        rs_json = response.json()
        return rs_json
