import logging

from actions.files import FilesActions
from actions.requests import RequestsActions
from actions.transactions import TransactionsActions
from helpers.authorization_helper import AuthorizationHelper

LOGGER = logging.getLogger(__name__)


class Application:

    def __init__(self, config):
        self.config = config
        self.auth_helper = AuthorizationHelper(self)
        self.transactions_actions = TransactionsActions(self)
        self.files_actions = FilesActions(self)
        self.requests_actions = RequestsActions(self)
        self.authorize()

    def authorize(self):
        LOGGER.info("Authorization process")
        self.auth_helper.authorize(username=self.config['authorization']['user']['username'],
                                   password=self.config['authorization']['user']['password'],
                                   role="user")
        self.auth_helper.authorize(username=self.config['authorization']['admin']['username'],
                                   password=self.config['authorization']['admin']['password'],
                                   role="admin")

    def destroy(self):
        LOGGER.info("Exit test")
