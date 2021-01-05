import logging
from actions.transactions import TransactionsActions
from actions.files import FilesActions
from actions.auth import AuthActions

LOGGER = logging.getLogger(__name__)


class Application:

    def __init__(self, config):
        self.config = config
        self.auth_actions = AuthActions(self)
        self.transactions_actions = TransactionsActions(self, self.auth_actions.request_util)
        self.files_actions = FilesActions(self, self.auth_actions.request_util)

    def destroy(self):
        LOGGER.info("Exit test")
