import requests
from requests import RequestException
import logging

from .utilities import is_ok, is_successful
from .exceptions import JWTMissingException
from .traverson import Traverson
from .encoders import CurationEncoder, SearchQueryEncoder
from .models import CurationLink, SearchQuery


class Client:

    def __init__(self, url=None):
        if url is None:
            raise Exception("You must provide the base url for the client to work")
        self._url = url

    def fetch_sample(self, accession):
        logging.debug("Getting sample with accession {} from {}".format(accession, self._url))
        traverson = Traverson(self._url)
        response = traverson \
            .follow("samples") \
            .follow("sample", params={"accession": accession}) \
            .get()
        if is_ok(response):
            # return dict_to_sample(response.json())
            return response.json()

        raise RequestException(response=response, message="An error occurred while fetching sample {}".format(accession))

    def persist_sample(self, sample, jwt=None):
        logging.debug("Submitting new sample to {}".format(self._url))
        if jwt is None:
            raise JWTMissingException
        traverson = Traverson(self._url)
        response = traverson \
            .follow("samples") \
            .get()

        if is_ok(response):
            headers = {
                "Authorization": "Bearer {}".format(jwt),
                "Content-Type": "application/json"
            }
            response = requests.post(response.url, json=sample, headers=headers)
            if is_successful(response):
                return response.json()

        raise response.raise_for_status()

    def update_sample(self, sample, jwt=None):
        # TODO: update the real samples
        logging.debug("Updating sample with accession {} on {}".format(sample["accession"], self._url))
        accession = sample["accession"]
        if jwt is None:
            raise JWTMissingException

        traverson = Traverson(self._url)
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
            if is_successful(response):
                return response.json()

        response.raise_for_status()

    def curate_sample(self, sample, curation_object, domain, jwt=None):
        logging.debug("Curating sample {} on {}".format(sample['accession'], self._url))
        if jwt is None:
            raise JWTMissingException

        accession = sample["accession"]
        curation_link = CurationLink(accession=accession, curation=curation_object, domain=domain)

        traverson = Traverson(self._url)
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
            json_body = CurationEncoder().default(curation_link)
            response = requests.post(response.url, json=json_body, headers=headers)
            if is_successful(response):
                return response.json()

        response.raise_for_status()

    def search(self, text=None, filters=None, page=0, size=50):
        query_object = SearchQuery(text=text, filters=filters, page=page, size=size)
        traverson = Traverson(self._url)
        response = traverson.follow("samples").get()
        if is_ok(response):
            response = requests.get(response.url, params=SearchQueryEncoder().default(query_object))
            if is_ok(response):
                return response.json()
        response.raise_for_status()


