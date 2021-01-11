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
        self.create_request(source_name, endpoint)

    @allure.step("Create new request from admin account")
    def create_request_by_admin(self, source_name, endpoint):
        LOGGER.info("Create new request from admin")
        endpoint = self.admin_base_url + endpoint
        self.create_request(source_name, endpoint)

    def create_request(self, source_name, endpoint):
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

    @allure.step("Update conversion rate of created request as an admin")
    def update_conversion_rate(self, source_name, endpoint):
        LOGGER.info("Update conversion rate of created request as an admin")
        endpoint = self.admin_base_url + endpoint + f"{self.request_id}"
        headers = {"Content-Type": "application/json"}
        source_file = Path("../data") / source_name
        with open(source_file, "rb") as data:
            self.response = self.request_util.patch(endpoint, headers=headers, data=data)
        self.request_id = self.response['data']['id']

    @allure.step("Check if rate of request was updated")
    def verify_request_rate_update(self, rate):
        LOGGER.info("Check if rate of request was updated")
        endpoint = self.user_base_url + f"requests/{self.request_id}"
        self.response = self.request_util.get(endpoint)
        response_rate = self.response['data']['request']['request']['rate']
        response_id = self.response['data']['request']['request']['id']
        assert self.request_id == response_id, f"Test update request failed. " \
                                               f"Expected request ID: {self.request_id}, " \
                                               f"Actual request ID: {response_id}"
        assert response_rate == rate, f"Test update request failed. " \
                                      f"Expected request rate: {rate}, " \
                                      f"Actual request rate: {response_rate}"

    @allure.step("Execute pending request as admin")
    def execute_request(self):
        LOGGER.info("Execute pending request as admin")
        endpoint = self.admin_base_url + f"requests/execute/{self.request_id}"
        self.response = self.request_util.post(endpoint)
        self.request_id = self.response['data']['id']

    @allure.step("Cancel pending request as admin")
    def cancel_request(self):
        LOGGER.info("Cancel pending request as admin")
        endpoint = self.admin_base_url + f"requests/cancel/{self.request_id}"
        self.response = self.request_util.post(endpoint)
        self.request_id = self.response['data']['id']

    @allure.step("Check request status")
    def verify_request_status(self, status):
        LOGGER.info("Check request status")
        endpoint = self.user_base_url + f"requests/{self.request_id}"
        self.response = self.request_util.get(endpoint)
        response_status = self.response['data']['request']['request']['status']
        response_id = self.response['data']['request']['request']['id']
        assert self.request_id == response_id, f"Test change request status failed. " \
                                               f"Expected request ID: {self.request_id}, " \
                                               f"Actual request ID: {response_id}"
        assert status == response_status, f"Test change request status failed. " \
                                          f"Expected request status: {status}, " \
                                          f"Actual request status: {response_status}"
