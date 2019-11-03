from os import environ

class AuthService:
    def __init__(self):
        # TODO: Change from config file over to os.environment
        self.mockKey = environ['TOKEN']

    def authenticate(self, in_key):
        return self.mockKey == in_key


