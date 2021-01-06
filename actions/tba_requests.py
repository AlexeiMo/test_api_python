import logging
from pathlib import Path

import allure

LOGGER = logging.getLogger(__name__)


class TBARequestsActions:
    response = None
    request_id = None

    def __init__(self, app, request_util):
        self.app = app
        self.request_util = request_util
        self.base_url = self.app.config['tba_requests']['host']

    @allure.step("Create new request from user account")
    def create_request(self, source_name):
        LOGGER.info("Create new request from user account")
        endpoint = self.base_url + "tba-requests"
        headers = {"Content-Type": "application/json"}
        source_file = Path("../data") / source_name
        with open(source_file, "rb") as data:
            self.response = self.request_util.post(endpoint, headers=headers, data=data)
        self.request_id = self.response['data']['id']

    @allure.step("Check if request was created correctly")
    def verify_new_request(self):
        LOGGER.info("Check if request was created correctly")
        endpoint = self.base_url + f"requests/{self.request_id}"
        self.response = self.request_util.get(endpoint)
        request_type = self.response['data']['request']['request']['subject']
        response_id = self.response['data']['request']['request']['id']
        assert self.request_id == response_id, f"Test create TBA request failed. " \
                                               f"Expected request ID: {self.request_id}, " \
                                               f"Actual request ID: {response_id}"
        assert request_type == "TBA", f"Test create TBA request failed. " \
                                      f"Expected request type: TBA, " \
                                      f"Actual request type: {request_type}"
