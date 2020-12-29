class Group:

    def __init__(self, auth_url=None, base_url=None, username=None, password=None):
        self.auth_url = auth_url
        self.base_url = base_url
        self.username = username
        self.password = password

    def __repr__(self):
        return f"{self.auth_url}, {self.base_url}, {self.username}, {self.password}"
