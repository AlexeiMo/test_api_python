import logging

import allure

LOGGER = logging.getLogger(__name__)


class TransactionsActions:
    response = None

    def __init__(self, app, request_util):
        self.app = app
        self.base_url = app.config['transactions']['host']
        self.request_util = request_util

    @allure.step("Get transaction from user profile by id")
    def get_transaction(self, transaction_id):
        LOGGER.info("Get transaction from user profile by id")
        endpoint = self.base_url + f"transactions/{transaction_id}"
        self.response = self.request_util.get(endpoint)

    @allure.step("Verify match of response transaction to requested one")
    def verify_response(self, transaction_id):
        LOGGER.info("Verify match of response transaction to requested one")
        assert self.response['data']['id'] == transaction_id, f"Test get transaction by id failed. " \
                                                              f"Expected id: {transaction_id}, " \
                                                              f"Actual id: {self.response['data']['id']}"
