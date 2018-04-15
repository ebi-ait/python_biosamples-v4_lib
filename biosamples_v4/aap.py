import requests
import logging
import jwt
import pytz
from datetime import datetime, timedelta
from .utilities import is_ok


class Client:
    """
    Client to interact with the AAP (Authentication and Authorization) service used in BioSamples
    """
    def __init__(self, username=None, password=None, url=None):
        """
        Create a new instance of the client using some details for the authentication
        :param username: the username of the user
        :type username: str
        :param password: the password
        :type password: str
        :param url: the url for the AAP authentication, usually finishing with '/auth'
        :type url: str
        """
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
        """
        Get a new token from the AAP domain or a cached one if not expired
        :return: the token
        :rtype: str
        """
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
        """
        Checks if the provided token is expired
        :param token: the token to check
        :type token: str
        :return: if the token is expired
        :rtype: bool
        """
        decoded_token = Client.decode_token(token)
        expiration_time = datetime.fromtimestamp(decoded_token['exp'], pytz.utc)
        return expiration_time < datetime.now(pytz.utc)+timedelta(minutes=15)

    @staticmethod
    def decode_token(token):
        """
        Decodes the provided token
        :param token: the token to decode
        :type token: str
        :return: the decoded token
        :rtype dict
        """
        return jwt.decode(token, verify=False)
