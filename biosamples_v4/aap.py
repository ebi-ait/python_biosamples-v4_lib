import requests
import logging
import jwt
import pytz
from datetime import datetime, timedelta
from .utilities import is_ok, is_successful


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
        self.baseurl = url
        self.auth_url = self._relative_path("auth")
        self.token = None

    def _relative_path(self, *args):
        return "{}/{}".format(self.baseurl, "/".join(args))

    def _token_header(self):
        return {
            "Authorization": "Bearer {}".format(self.get_token())
        }

    def _get_clean_or_rise(self, url, headers=None):
        final_headers = self._token_header()
        if headers is not None:
            final_headers = {**final_headers, **headers}

        response = requests.get(url, headers=final_headers)
        if is_successful(response):
            return response.json()

        raise response.raise_for_status()

    def _post_clean_or_rise(self, url, json, headers=None):
        final_headers = self._token_header()
        if headers is not None:
            final_headers = {**final_headers, **headers}

        response = requests.post(url, json=json, headers=final_headers)
        if is_successful(response):
            return response.json()

        raise response.raise_for_status()

    def create_domain(self, name, description):
        """
        Create an AAP domain with the specific name and description
        :param str name: the name of the domain
        :param str description: the description for the domain
        :return: response content
        :raises HttpError: if the response is not 2xx
        """
        domain_info = {
            "domainName": name,
            "domainDesc": description
        }

        domain_url = self._relative_path("domains")
        return self._post_clean_or_rise(url=domain_url, json=domain_info)

    def get_user_details(self):
        """
        A 'GET' request to get user details based on user name.
        :return: the user details
        """
        user_details_url = self._relative_path("users", self.username)
        return self._get_clean_or_rise(user_details_url)

    def get_user_managed_domains(self):
        """
        Get logged in user management domains.
        :return: the list of domains
        :rtype: list
        :raises Exception: if an error occurred while retriving the content
        """
        user_domains_management_url = self._relative_path("my", "management")
        return self._get_clean_or_rise(url=user_domains_management_url)

    def get_user_membership_domains(self):
        """
        Get logged in user membership domains.
        :return: the list of domains
        :rtype: list
        :raises Exception: if an error occurred while retriving the content
        """
        user_domains_membership_url = self._relative_path("my", "domains")
        return self._get_clean_or_rise(url=user_domains_membership_url)

    def get_token(self):
        """
        Get a new token from the AAP domain or a cached one if not expired
        :return: the token
        :rtype: str
        """
        if self.token is None or Client.is_token_expired(self.token):
            logging.debug("Username {} getting token from {}".format(self.username, self.auth_url))
            response = requests.get(self.auth_url, auth=(self.username, self.password))
            if is_ok(response):
                logging.debug("Got token correctly")
                self.token = response.text
                return self.token
            return response.raise_for_status()
        else:
            logging.debug("Using cached token for user {} taken from url {}".format(self.username, self.auth_url))
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
        return expiration_time < datetime.now(pytz.utc) + timedelta(minutes=15)

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
