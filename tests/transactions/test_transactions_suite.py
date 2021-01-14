import pytest


@pytest.mark.transactions
class TestTransactionsSuite(object):

    @pytest.mark.tcid1
    def test_get_transaction_by_id(self, app):
        tr_id = app.config["transactions"]["id"]
        response = app.transactions_actions.get_transaction(tr_id)
        app.transactions_actions.verify_response(response, tr_id)
