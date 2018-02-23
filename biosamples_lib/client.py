import requests

from biosamples_lib.utilities import is_ok
from biosamples_lib.traverson import Traverson
from biosamples_lib import aap_client
from biosamples_lib.Encoders import CurationObjectEncoder


class Client:
    def __init__(self, baseurl=None):
        if baseurl is None:
            raise Exception("You must provide the base url for the client to work")
        self._baseurl = baseurl

    def fetch_sample(self, accession):
        traverson = Traverson(self._baseurl)
        response = traverson \
            .follow("samples") \
            .follow("sample", params={"accession": accession}) \
            .get()
        return response

    def persist_sample(self, sample):
        print("Submitting sample with accession {}".format(sample["accession"]))
        jwt = aap_client.get_token()
        traverson = Traverson(self._baseurl)
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

    def update_sample(self, sample, jwt=None):
        # TODO: update the real samples
        accession = sample["accession"]
        if jwt is None:
            jwt = aap_client.get_token()
        traverson = Traverson(self._baseurl)
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

    def curate_sample(self, sample, curation_object, jwt=None):
        accession = sample["accession"]
        if jwt is None:
            jwt = aap_client.get_token()
        traverson = Traverson(self._baseurl)
        response = traverson \
            .follow("samples") \
            .follow("sample", params={"accession": accession}) \
            .follow("curationLinks") \
            .get()
        if is_ok(response):
            headers = {
                "Authorization": "Bearer {}".format(jwt),
                "Content-type": "application/json"
            }
            json_body = CurationObjectEncoder().default(curation_object)
            response = requests.post(response.url, json=json_body, headers=headers)
        return response
