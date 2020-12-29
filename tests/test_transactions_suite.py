import pytest

from model.group import Group


@pytest.mark.transactions
class TestTransactionSuite:

    def test_get_transaction_by_id(self, app):
        app.transactions_actions.authorize_user(Group(username=app.config['http']['username'],
                                                      password=app.config['http']['password']))
        app.transactions_actions.get_transaction(transaction_id=app.config['transactions']['id'])
        app.transactions_actions.verify_response(transaction_id=app.config['transactions']['id'])
