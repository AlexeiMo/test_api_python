import logging

import allure

from helpers.requests_helper import RequestsHelper

LOGGER = logging.getLogger(__name__)


class RequestsActions:

    def __init__(self, app):
        self.app = app
        self.request_helper = RequestsHelper(app)

    @allure.step("Create new request")
    def create_request(self, source_name, endpoint, role):
        LOGGER.info("Create new request")
        response = self.request_helper.create_request(source_name, endpoint, role)
        request_id = response['data']['id']
        return request_id

    @allure.step("Check if request was created correctly")
    def verify_new_request(self, request_id, request_type):
        LOGGER.info("Check if request was created correctly")
        response = self.request_helper.get_request_by_id(request_id, role="admin")
        response_type = response['data']['request']['request']['subject']
        response_id = response['data']['request']['request']['id']
        assert request_id == response_id, f"Test create request failed. " \
                                          f"Expected request ID: {request_id}, " \
                                          f"Actual request ID: {response_id}"
        assert response_type == request_type, f"Test create request failed. " \
                                              f"Expected request type: f{request_type}, " \
                                              f"Actual request type: {response_type}"

    @allure.step("Update conversion rate of created request as an admin")
    def update_conversion_rate(self, source_name, endpoint, request_id):
        LOGGER.info("Update conversion rate of created request as an admin")
        response = self.request_helper.update_request_rate_by_id(source_name, endpoint, request_id)
        request_id = response['data']['id']
        return request_id

    @allure.step("Check if rate of request was updated")
    def verify_request_rate_update(self, request_id, rate):
        LOGGER.info("Check if rate of request was updated")
        response = self.request_helper.get_request_by_id(request_id, role="admin")
        response_rate = response['data']['request']['request']['rate']
        response_id = response['data']['request']['request']['id']
        assert request_id == response_id, f"Test update request failed. " \
                                          f"Expected request ID: {request_id}, " \
                                          f"Actual request ID: {response_id}"
        assert response_rate == rate, f"Test update request failed. " \
                                      f"Expected request rate: {rate}, " \
                                      f"Actual request rate: {response_rate}"

    @allure.step("Execute pending request as admin")
    def execute_request(self, request_id):
        LOGGER.info("Execute pending request as admin")
        self.request_helper.change_request_status_by_id(request_id,
                                                        status="execute")

    @allure.step("Cancel pending request as admin")
    def cancel_request(self, request_id):
        LOGGER.info("Cancel pending request as admin")
        self.request_helper.change_request_status_by_id(request_id,
                                                        status="cancel")

    @allure.step("Check request status")
    def verify_request_status(self, request_id, status):
        LOGGER.info("Check request status")
        response = self.request_helper.get_request_by_id(request_id, role="admin")
        response_status = response['data']['request']['request']['status']
        response_id = response['data']['request']['request']['id']
        assert request_id == response_id, f"Test change request status failed. " \
                                          f"Expected request ID: {request_id}, " \
                                          f"Actual request ID: {response_id}"
        assert status == response_status, f"Test change request status failed. " \
                                          f"Expected request status: {status}, " \
                                          f"Actual request status: {response_status}"
