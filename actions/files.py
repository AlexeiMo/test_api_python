import logging
from pathlib import Path

import allure

from clients.files_client import FilesClient

LOGGER = logging.getLogger(__name__)


class FilesActions:

    def __init__(self, app):
        self.app = app
        self.files_client = FilesClient(app)

    @allure.step("Upload user file to server")
    def upload_file(self, filename, content_type, user_id):
        LOGGER.info("Upload user file to server")
        response = self.files_client.upload_file_from_user(filename, content_type, user_id)
        file_id = response["data"]["id"]
        return file_id

    @allure.step("Verify match of response file info to created one")
    def verify_file_upload(self, user_id, file_id):
        LOGGER.info("Verify match of response file info to created one")
        response = self.files_client.get_all_files_of_user(user_id)
        id_list = [item["id"] for item in response["data"]["items"]]
        assert file_id in id_list, f"Test upload file failed. " \
                                   f"There's no file with id {file_id} on server."

    @allure.step("Delete file from server")
    def delete_file(self, file_id):
        LOGGER.info("Delete file from server")
        self.files_client.delete_file_by_id(file_id)

    @allure.step("Verify if file was deleted")
    def verify_file_delete(self, user_id, file_id):
        LOGGER.info("Verify if file was deleted")
        response = self.files_client.get_all_files_of_user(user_id)
        id_list = [item["id"] for item in response["data"]["items"]]
        assert file_id not in id_list, f"Test delete file failed. " \
                                       f"File with id {file_id} was not deleted from server."
