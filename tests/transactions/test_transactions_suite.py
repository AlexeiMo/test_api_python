import pytest


@pytest.mark.transactions
class TestTransactionsSuite(object):

    @pytest.fixture(scope="function")
    def auth_user(self, app):
        app.auth_actions.authorize_user(username=app.config['authorization']['user']['username'],
                                        password=app.config['authorization']['user']['password'])

    @pytest.mark.tcid1
    def test_get_transaction_by_id(self, app, auth_user):
        app.transactions_actions.get_transaction(transaction_id=app.config['transactions']['id'])
        app.transactions_actions.verify_response(transaction_id=app.config['transactions']['id'])
