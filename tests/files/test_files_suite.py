import pytest


@pytest.mark.files
class TestFilesSuite(object):

    @pytest.mark.tcid2
    def test_upload_file(self, app):
        filename = app.config['files']['filename']
        content_type = app.config['files']['content_type']
        user_id = app.config['authorization']['user']['user_id']
        file_id = app.files_actions.upload_file(filename, content_type, user_id)
        app.files_actions.verify_file_upload(user_id, file_id)

    @pytest.mark.tcid3
    def test_delete_file(self, app):
        filename = app.config['files']['filename']
        content_type = app.config['files']['content_type']
        user_id = app.config['authorization']['user']['user_id']
        file_id = app.files_actions.upload_file(filename, content_type, user_id)
        app.files_actions.delete_file(file_id)
        app.files_actions.verify_file_delete(user_id, file_id)
