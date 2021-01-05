import logging

from utilities.requests_utility import RequestUtility
from model.group import Group

import allure

LOGGER = logging.getLogger(__name__)


class TransactionsActions:
    response = None

    def __init__(self, app):
        self.app = app
        self.request_util = RequestUtility(Group(auth_url=app.config['http']['host_auth'],
                                                 base_url=app.config['transactions']['host']
                                                 ))

    @allure.step("Authorize user to get access token")
    def authorize_user(self, group):
        LOGGER.info("Authorize user to get access token")
        self.request_util.authorize(username=group.username, password=group.password)

    @allure.step("Get transaction from user profile by id")
    def get_transaction(self, transaction_id):
        LOGGER.info("Get transaction from user profile by id")
        self.response = self.request_util.get(f"transactions/{transaction_id}")

    @allure.step("Verify match of response transaction to requested one")
    def verify_response(self, transaction_id):
        LOGGER.info("Verify match of response transaction to requested one")
        assert self.response['data']['id'] == transaction_id, f"Test get transaction by id failed. " \
                                                              f"Expected id: {transaction_id}, " \
                                                              f"Actual id: {self.response['data']['id']}"
