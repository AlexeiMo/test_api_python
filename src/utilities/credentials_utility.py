import os


class CredentialsUtility(object):

    def __init__(self):
        pass

    @staticmethod
    def get_api_keys():

        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')

        if not email or not password:
            raise Exception("The API credentials 'EMAIL' and 'PASSWORD' must be in env variable")
        else:
            return {'email': email, 'password': password}
