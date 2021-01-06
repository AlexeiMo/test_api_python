import pytest


@pytest.mark.ebanq_qa
class TestEbanqQaSuite(object):
    @pytest.fixture(scope="function")
    def auth_user(self, app):
        app.auth_actions.authorize_user(username=app.config['authorization']['user']['username'],
                                        password=app.config['authorization']['user']['password'])

    @pytest.fixture(scope="function")
    def auth_admin(self, app):
        app.auth_actions.authorize_user(username=app.config['authorization']['admin']['username'],
                                        password=app.config['authorization']['admin']['password'])

    @pytest.mark.transactions
    def test_get_transaction_by_id(self, app, auth_user):
        app.transactions_actions.get_transaction(transaction_id=app.config['transactions']['id'])
        app.transactions_actions.verify_response(transaction_id=app.config['transactions']['id'])

    @pytest.mark.files
    def test_upload_file(self, app, auth_user):
        app.files_actions.upload_file(filename=app.config['files']['filename'],
                                      content_type=app.config['files']['content_type'],
                                      user_id=app.config['authorization']['user']['user_id'])
        app.files_actions.verify_file_upload()

    @pytest.mark.files
    def test_delete_file(self, app, auth_user):
        app.files_actions.upload_file(filename=app.config['files']['filename'],
                                      content_type=app.config['files']['content_type'],
                                      user_id=app.config['authorization']['user']['user_id'])
        app.files_actions.verify_file_upload()
        app.files_actions.delete_file()
        app.files_actions.verify_file_delete()

    @pytest.mark.tba_requests
    def test_create_tba_request(self, app, auth_user):
        app.requests_actions.create_request_by_user(source_name=app.config['tba_requests']['source_name'],
                                                    endpoint="tba-requests")
        app.requests_actions.verify_new_request(request_type="TBA")

    def test_create_tbu_request(self, app, auth_admin):
        app.requests_actions.create_request_by_admin(source_name=app.config['tbu_requests']['source_name'],
                    endpoint="tbu_requests/user/" + app.config['authorization']['user']['user_id'])
        app.requests_actions.verify_new_request(request_type="TBU")
