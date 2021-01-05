import logging
from pathlib import Path

import allure

LOGGER = logging.getLogger(__name__)


class FilesActions:
    response = None
    file_id = None

    def __init__(self, app, request_util):
        self.app = app
        self.request_util = request_util
        self.base_url = app.config["files"]["host"]

    @allure.step("Upload user file to server")
    def upload_file(self, filename, content_type):
        LOGGER.info("Upload user file to server")
        endpoint = self.base_url + "files/private/42337c0a-4c44-4be7-8b2e-cf92ac4388cc"
        file_to_open = Path("../data") / filename
        with open(file_to_open, "rb") as file:
            files = {"file": (filename, file, content_type)}
            self.response = self.request_util.post_file(endpoint, files=files)
        self.file_id = self.response["data"]["id"]

    @allure.step("Verify match of response file info to created one")
    def verify_file_upload(self):
        LOGGER.info("Verify match of response file info to created one")
        self.get_all_files()
        id_list = [item["id"] for item in self.response["data"]["items"]]
        assert self.file_id in id_list, f"Test upload file failed. " \
                                        f"There's no file with id {self.file_id} on server."

    @allure.step("Delete file from server")
    def delete_file(self):
        LOGGER.info("Delete file from server")
        endpoint = self.base_url + f"files/{self.file_id}"
        self.response = self.request_util.delete(endpoint)

    @allure.step("Verify if file was deleted")
    def verify_file_delete(self):
        LOGGER.info("Verify if file was deleted")
        self.get_all_files()
        id_list = [item["id"] for item in self.response["data"]["items"]]
        assert self.file_id not in id_list, f"Test delete file failed. " \
                                            f"File with id {self.file_id} wasn't deleted from server."

    @allure.step("Get all files from server")
    def get_all_files(self):
        LOGGER.info("Verify match of response file info to created one")
        endpoint = self.base_url + "users/42337c0a-4c44-4be7-8b2e-cf92ac4388cc"
        self.response = self.request_util.get(endpoint)
