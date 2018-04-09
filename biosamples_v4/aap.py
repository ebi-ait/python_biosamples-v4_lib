import requests
import logging
import jwt
from datetime import datetime
from .utilities import is_ok


class Client:
    def __init__(self, username=None, password=None, url=None):
        if username is None:
            raise Exception("An AAP username has not been provided")
        if password is None:
            raise Exception("The password associated with the username is missing ")
        if url is None:
            raise Exception("A url to use with the client is missing")
        self.username = username
        self.password = password
        self.url = url
        self.token = None

    def get_token(self):
        if self.token is None or Client.is_token_expired(self.token):
            logging.debug("Username {} getting token from {}".format(self.username, self.url))
            response = requests.get(self.url, auth=(self.username, self.password))
            if is_ok(response):
                logging.debug("Got token correctly")
                self.token = response.text
                return self.token
            return response.raise_for_status()
        else:
            logging.debug("Using cached token for user {} taken from url {}".format(self.username, self.url))
            return self.token

    @staticmethod
    def is_token_expired(token):
        decoded_token = Client.decode_token(token)
        expiration_time = datetime.fromtimestamp(decoded_token['exp'])
        return expiration_time < datetime.utcnow()

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, verify=False)
