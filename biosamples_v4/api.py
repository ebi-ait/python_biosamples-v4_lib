import requests
import logging

from .utilities import is_ok, is_successful, is_not_found
from .exceptions import JWTMissingException
from .traverson import Traverson, SampleSearchResultsPageNavigator, SampleSearchResultsCursor
from .encoders import CurationEncoder, SearchQueryEncoder
from .models import CurationLink, SearchQuery


def _prepare_params(**kwargs):
    params = {}
    for k, v in kwargs.items():
        if v is not None:
            params[k] = v
    return params


def _clean_sample(sample, fields=None):
    """
    Clean a sample resource from unnecessary fields

    :param sample: the sample to clean
    :type sample: dict
    :return: Sample cleaned from unnecessary params
    :rtype: dict
    """

    if fields is None:
        fields = ['_links', 'releaseDate', 'updateDate', 'taxId']

    for f in fields:
        if f in sample:
            del sample[f]

    return sample


class Client:
    """
    Client to interact with the BioSamples API.

    You can use this client to do some tasks like get a sample by accession, submit samples or update them,
    create curation as well as search for samples
    """

    def __init__(self, url=None):
        if url is None:
            raise Exception("You must provide the base url for the client to work")
        self._url = url

    def fetch_sample(self, accession, curation_domains=None, jwt=None):
        """
        GET sample by accession

        :param accession: the accession of the samples, e.g. SAMEA123456
        :type accession: str
        :param jwt: the token to use to retrieve the sample when it's private
        :type jwt: str
        :param curation_domains: A list of curation domain to use when getting the samples
        :type curation_domains: list or None
        :return: the sample in json format
        :rtype: dict
        :raises: Exception if the response is not 200
        """
        logging.debug("Getting sample with accession {} from {}".format(accession, self._url))

        sample_params = _prepare_params(accession=accession)

        traverson = Traverson(self._url, jwt=jwt)
        traverson \
            .follow("samples") \
            .follow("sample", params=sample_params)

        if curation_domains is not None:
            curation_params = _prepare_params(curationdomain=curation_domains)
            traverson.follow("curationDomain", params=curation_params)

        response = traverson.get()
        if is_ok(response):
            # return dict_to_sample(response.json())
            return response.json()

        raise response.raise_for_status()

    def fetch_raw(self, accession, jwt=None):
        """
        GET sample by accession without any curation applied

        :param accession: the accession of the samples, e.g. SAMEA123456
        :type accession: str
        :param jwt: the token to use to retrieve the sample when it's private
        :type jwt: str
        :return: the sample in json format
        :rtype: dict
        :raises: Exception if the response is not 200
        """
        return self.fetch_sample(accession=accession, jwt=jwt, curation_domains=[])

    def persist_sample(self, sample, jwt=None):
        """
        POST new sample to biosample

        :param sample: the sample to POST
        :type sample: dict
        :param jwt: the token to use to store the sample
        :type jwt: str
        :return: the stored sample including the provided accession
        :rtype: dict
        :raises: Exception if the response is not successful
        """
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
            response = requests.post(response.url, json=_clean_sample(sample), headers=headers)
            if is_successful(response):
                return response.json()

        raise response.raise_for_status()

    def update_sample(self, sample, jwt=None):
        """
        PUT (Update) sample in BioSamples

        :param sample: the sample to update
        :type sample: dict
        :param jwt: the token to use for the update
        :type jwt: str
        :return: the updated sample
        :rtype: dict
        :raises: Exception if the response is not successful
        """
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
            response = requests.put(response.url, json=_clean_sample(sample), headers=headers)
            if is_successful(response):
                return response.json()

        response.raise_for_status()

    def curate_sample(self, sample, curation_object, domain, jwt=None):
        """
        Generate a curationLink between a sample and a curation object using a specific domain

        :param sample: the sample to curate
        :param curation_object: the curation object to apply
        :param domain: the domain to use for the curation action
        :param jwt: the token to authorize the curation
        :return: The generated curation link
        :rtype: dict
        :raises: Exception if is not possible to find the curationLinks link or
        storing the curation link wasn't successful
        """
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
        """
        Search for samples using a specific text, filters

        :param text: the text to search for
        :type text: str
        :param filters: the list of filters to add to the search query
        :type filters: list
        :param page: the starting page for the results
        :type page: int
        :param size: the number of results per page
        :type size: int
        :param jwt: the token to use for authorization, not required to get public samples
        :type jwt: str
        :return: the first page of the search result
        :rtype: dict
        :raises: Exception if the search wasn't successful
        """
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
        :rtype: SampleSearchResultsPageNavigator
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
        :rtype: SampleSearchResultCursor
        """
        return SampleSearchResultsCursor(self.search(text=text, filters=filters, size=size, jwt=jwt))
