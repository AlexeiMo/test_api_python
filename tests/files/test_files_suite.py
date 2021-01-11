import pytest


@pytest.mark.files
class TestFilesSuite(object):

    @pytest.fixture(scope="function")
    def auth_user(self, app):
        app.auth_actions.authorize_user(username=app.config['authorization']['user']['username'],
                                        password=app.config['authorization']['user']['password'])

    @pytest.mark.tcid2
    def test_upload_file(self, app, auth_user):
        app.files_actions.upload_file(filename=app.config['files']['filename'],
                                      content_type=app.config['files']['content_type'],
                                      user_id=app.config['authorization']['user']['user_id'])
        app.files_actions.verify_file_upload()

    @pytest.mark.tcid3
    def test_delete_file(self, app, auth_user):
        app.files_actions.upload_file(filename=app.config['files']['filename'],
                                      content_type=app.config['files']['content_type'],
                                      user_id=app.config['authorization']['user']['user_id'])
        app.files_actions.verify_file_upload()
        app.files_actions.delete_file()
        app.files_actions.verify_file_delete()
