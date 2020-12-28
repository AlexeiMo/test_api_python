import pytest
import logging
from src.helpers.transactions_helper import TransactionsHelper

LOGGER = logging.getLogger(__name__)


@pytest.mark.transactions
class TestTransactionSuite():

    def test_get_transaction_by_id(self):
        tr_id = 499262
        transaction_helper = TransactionsHelper()
        response = transaction_helper.get_transaction(tr_id)
        assert response['data']['id'] == tr_id, f"Test get transaction by id failed. " \
                                                f"Expected id: {tr_id}, " \
                                                f"Actual id: {response['data']['id']}"
