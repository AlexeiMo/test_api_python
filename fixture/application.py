import logging
from actions.transactions import TransactionsActions

LOGGER = logging.getLogger(__name__)


class Application:

    def __init__(self, config):
        self.config = config
        self.transactions_actions = TransactionsActions(self)

    def destroy(self):
        LOGGER.info("Exit test")
