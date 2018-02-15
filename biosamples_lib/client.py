import requests

from biosamples_lib import BASEURL
from biosamples_lib.utilities import is_ok
from biosamples_lib.traverson import Traverson
from biosamples_lib import aap_client


def fetch_sample(accession):
    traverson = Traverson(BASEURL)
    response = traverson \
        .follow("samples") \
        .follow("sample", params={"accession": accession}) \
        .get()
    return response


def persist_sample(sample):
    print("Submitting sample with accession {}".format(sample["accession"]))
    jwt = aap_client.get_token()
    traverson = Traverson(BASEURL)
    response = traverson \
        .follow("samples") \
        .get()

    if is_ok(response):
        headers = {
            "Authorization": "Bearer {}".format(jwt),
            "Content-Type": "application/json"
        }
        response = requests.post(response.url, json=sample, headers=headers)

    return response


def update_sample(sample):
    # TODO: update the real samples
    accession = sample["accession"]
    jwt = aap_client.get_token()
    traverson = Traverson(BASEURL)
    response = traverson \
        .follow("samples") \
        .follow("sample", params={"accession": accession}) \
        .get()
    if is_ok(response):
        headers = {
            "Authorization": "Bearer {}".format(jwt),
            "Content-Type": "application/json"
        }
        response = requests.put(response.url, json=sample, headers=headers)
    return response
