import requests


class AapClient:
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

    def get_token(self):
        response = requests.get(self.url, auth=(self.username, self.password))
        if response.status_code == requests.codes.ok:
            return response.text
        return response
