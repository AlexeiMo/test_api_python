from src.utilities.requests_utility import RequestUtility


class TransactionsHelper(object):

    def __init__(self):
        self.request_util = RequestUtility()

    def get_transaction(self, transaction_id):
        return self.request_util.get(f"transactions/{transaction_id}")
