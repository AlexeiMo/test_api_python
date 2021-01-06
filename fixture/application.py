import logging
from actions.transactions import TransactionsActions
from actions.files import FilesActions
from actions.authorization import AuthorizationActions
from actions.tba_requests import TBARequestsActions

LOGGER = logging.getLogger(__name__)


class Application:

    def __init__(self, config):
        self.config = config
        self.auth_actions = AuthorizationActions(self)
        self.request_util = self.auth_actions.request_util
        self.transactions_actions = TransactionsActions(self, self.request_util)
        self.files_actions = FilesActions(self, self.request_util)
        self.tba_requests_actions = TBARequestsActions(self, self.request_util)

    def destroy(self):
        LOGGER.info("Exit test")
