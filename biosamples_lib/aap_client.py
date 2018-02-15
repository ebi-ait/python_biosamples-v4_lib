import requests

from biosamples_lib import AAP_TOKEN_URL
from biosamples_lib import AAP_USERNAME
from biosamples_lib import AAP_PASSWORD


def get_token(username=AAP_USERNAME, password=AAP_PASSWORD):
    response = requests.get(AAP_TOKEN_URL, auth=(username, password))
    if response.status_code == requests.codes.ok:
        return response.text
    return response
