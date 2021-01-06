import logging
from pathlib import Path

import allure

LOGGER = logging.getLogger(__name__)


class RequestsActions:
    response = None
    request_id = None

    def __init__(self, app, request_util):
        self.app = app
        self.request_util = request_util
        self.user_base_url = self.app.config['requests']['host_user']
        self.admin_base_url = self.app.config['requests']['host_admin']

    @allure.step("Create new request from user account")
    def create_request_by_user(self, source_name, endpoint):
        LOGGER.info("Create new request from user account")
        endpoint = self.user_base_url + endpoint
        headers = {"Content-Type": "application/json"}
        source_file = Path("../data") / source_name
        with open(source_file, "rb") as data:
            self.response = self.request_util.post(endpoint, headers=headers, data=data)
        self.request_id = self.response['data']['id']

    @allure.step("Create new request from admin account")
    def create_request_by_admin(self, source_name, endpoint):
        LOGGER.info("Create new request from admin")
        endpoint = self.admin_base_url + endpoint
        headers = {"Content-Type": "application/json"}
        source_file = Path("../data") / source_name
        with open(source_file, "rb") as data:
            self.response = self.request_util.post(endpoint, headers=headers, data=data)
        self.request_id = self.response['data']['id']

    @allure.step("Check if request was created correctly")
    def verify_new_request(self, request_type):
        LOGGER.info("Check if request was created correctly")
        endpoint = self.user_base_url + f"requests/{self.request_id}"
        self.response = self.request_util.get(endpoint)
        response_type = self.response['data']['request']['request']['subject']
        response_id = self.response['data']['request']['request']['id']
        assert self.request_id == response_id, f"Test create request failed. " \
                                               f"Expected request ID: {self.request_id}, " \
                                               f"Actual request ID: {response_id}"
        assert response_type == request_type, f"Test create request failed. " \
                                              f"Expected request type: f{request_type}, " \
                                              f"Actual request type: {response_type}"
