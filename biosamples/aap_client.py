import requests
import biosamples


def get_token(username=None, password=None, url=biosamples.AAP_TOKEN_URL):
    if username is None and password is None:
        raise Exception("You need to provide username and password to use the AAP client")
    response = requests.get(url, auth=(username, password))
    if response.status_code == requests.codes.ok:
        return response.text
    return response
