import pytest

from model.group import Group


@pytest.mark.ebanq_qa
class TestEbanqQaSuite(object):

    @pytest.mark.transactions
    def test_get_transaction_by_id(app):
        app.transactions_actions.authorize_user(Group(username=app.config['http']['username'],
                                                      password=app.config['http']['password']))
        app.transactions_actions.get_transaction(transaction_id=app.config['transactions']['id'])
        app.transactions_actions.verify_response(transaction_id=app.config['transactions']['id'])


    @pytest.mark.files
    def test_upload_file(app):
        app.files_actions.authorize_user(Group(username=app.config['http']['username'],
                                               password=app.config['http']['password']))
        app.files_actions.upload_file(filename=app.config['files']['filename'],
                                      content_type=app.config['files']['content_type'])
        app.files_actions.verify_response()
