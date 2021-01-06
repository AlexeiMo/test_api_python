import logging

from utilities.requests_utility import RequestUtility

import allure

LOGGER = logging.getLogger(__name__)


class AuthorizationActions:
    response = None

    def __init__(self, app):
        self.app = app
        self.request_util = RequestUtility()
        self.base_url = app.config['http']['host_auth']

    @allure.step("Authorize user to get access token")
    def authorize_user(self, username, password):
        LOGGER.info("Authorize user to get access token")
        self.request_util.authorize(self.base_url, username=username, password=password)
