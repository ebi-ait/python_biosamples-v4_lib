import requests
from requests import RequestException
import logging

from .utilities import is_ok, is_successful
from .exceptions import JWTMissingException
from .traverson import Traverson, SampleSearchResultsPageNavigator, SampleSearchResultsCursor
from .encoders import CurationEncoder, SearchQueryEncoder
from .models import CurationLink, SearchQuery


class Client:

    def __init__(self, url=None):
        if url is None:
            raise Exception("You must provide the base url for the client to work")
        self._url = url

    def fetch_sample(self, accession, jwt=None):
        logging.debug("Getting sample with accession {} from {}".format(accession, self._url))
        traverson = Traverson(self._url, jwt=jwt)
        response = traverson \
            .follow("samples") \
            .follow("sample", params={"accession": accession}) \
            .get()
        if is_ok(response):
            # return dict_to_sample(response.json())
            return response.json()

        raise response.raise_for_status()

    def persist_sample(self, sample, jwt=None):
        logging.debug("Submitting new sample to {}".format(self._url))
        if jwt is None:
            raise JWTMissingException
        traverson = Traverson(self._url, jwt=jwt)
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

        traverson = Traverson(self._url, jwt=jwt)
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

        traverson = Traverson(self._url, jwt=jwt)
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

    def search(self, text=None, filters=None, page=0, size=20, jwt=None):
        query_object = SearchQuery(text=text, filters=filters, page=page, size=size)
        traverson = Traverson(self._url, jwt=jwt)
        response = traverson.follow("samples").get()
        if is_ok(response):
            response = requests.get(response.url, params=SearchQueryEncoder().default(query_object))
            if is_ok(response):
                return response.json()
        response.raise_for_status()

    def search_navigator(self, text=None, filters=None, page=0, size=20, jwt=None):
        """
        Return a search result in the form of navigator
        :param text: the text to search for
        :param filters: the filters to apply
        :type filters: list
        :param page: the starting page, default is 0
        :type page: int
        :param size: the number of results for page
        :type size: int
        :param jwt: the token to use for the search
        :type jwt: str
        :return: A page navigator for the results
        :rtype SampleSearchResultsPageNavigator
        """
        return SampleSearchResultsPageNavigator(self.search(text=text, filters=filters, page=page, size=size, jwt=jwt))

    def search_cursor(self, text=None, filters=None, size=20, jwt=None):
        """
        Return a search result in the form of cursor
        :param text: the text to search for
        :param filters: the filters to apply
        :type filters: list
        :param size: the number of results for page
        :type size: int
        :param jwt: the token to use for the search
        :type jwt: str
        :return: A cursor for the results
        :rtype SampleSearchResultCursor
        """
        return SampleSearchResultsCursor(self.search(text=text, filters=filters, size=size, jwt=jwt))
