import logging
from pathlib import Path

from utilities.requests_utility import RequestUtility
from model.group import Group

import allure

LOGGER = logging.getLogger(__name__)


class FilesActions:
    response = None

    def __init__(self, app):
        self.app = app
        self.request_util = RequestUtility(Group(auth_url=app.config['http']['host_auth'],
                                                 base_url=app.config['files']['host']
                                                 ))

    @allure.step("Authorize user to get access token")
    def authorize_user(self, group):
        LOGGER.info("Authorize user to get access token")
        self.request_util.authorize(username=group.username, password=group.password)

    @allure.step("Upload user file to server")
    def upload_file(self, filename, content_type):
        LOGGER.info("Upload user file to server")
        file_to_open = Path("../data") / filename
        with open(file_to_open, "rb") as file:
            files = {"file": (filename, file, content_type)}
            self.response = self.request_util.post_file("files/private/42337c0a-4c44-4be7-8b2e-cf92ac4388cc",
                                                        files=files)

    @allure.step("Verify match of response file info to created one")
    def verify_response(self):
        LOGGER.info("Verify match of response file info to created one")
        file_id = self.response["data"]["id"]
        self.response = self.request_util.get("users/42337c0a-4c44-4be7-8b2e-cf92ac4388cc")
        id_list = [item["id"] for item in self.response["data"]["items"]]
        assert file_id in id_list, f"Test upload file failed. " \
                                   f"There's no file with id {file_id} on server."
