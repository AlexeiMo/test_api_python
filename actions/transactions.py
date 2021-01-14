import logging
import allure
from helpers.transactions_helper import TransactionsHelper

LOGGER = logging.getLogger(__name__)


class TransactionsActions:

    def __init__(self, app):
        self.app = app
        self.transactions_helper = TransactionsHelper(app)

    @allure.step("Get transaction from user profile by id")
    def get_transaction(self, tr_id):
        LOGGER.info("Get transaction from user profile by id")
        response = self.transactions_helper.get_transaction_by_id(tr_id)
        tr_id = response["data"]["id"]
        return tr_id

    @allure.step("Verify match of response transaction to requested one")
    def verify_response(self, response_tr_id, tr_id):
        LOGGER.info("Verify match of response transaction to requested one")
        assert response_tr_id == tr_id, f"Test get transaction by id failed. " \
                                                f"Expected id: {tr_id}, " \
                                                f"Actual id: {response_tr_id}"
