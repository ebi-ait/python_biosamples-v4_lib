import requests
import requests_cache
import re
import logging
from .utilities import is_ok

requests_cache.install_cache(cache_name='biosamples-cache', backend='sqlite', expire_after=180)


class Utils:

    @staticmethod
    def get_hal_session(jwt=None):
        """
        Generate a hal+json session to use for BioSamples including a potential JWT token
        :param jwt: optional JWT tokent to embed in the session
        :type jwt: str
        :return: a request session with hal+json headers and optional authorization header
        :rtype: Session
        """
        session = requests.Session()
        session.headers.update({
            "Accept": "application/hal+json",
            "Content-Type": "application/hal+json"
        })

        if jwt is not None:
            session.headers.update({
                "Authorization": "Bearer {}".format(jwt)
            })
        return session

    @staticmethod
    def populate_url(link, params, params_regex='{\?([A-Za-z0-9,]+)}'):
        """
        method to generate an expanded version of a parameterized link
        :param link: the paramaterized link
        :param params: the params to use for the expantion
        :return: the expanded url
        """
        qp_match = re.search(params_regex, link)
        query_params = []
        if qp_match:
            query_params = qp_match.group(1).split(",")
        final_url = re.sub(params_regex, "", link)
        final_url = final_url.format(**params)
        if len(query_params) > 0:
            query_string = []
            for qp in query_params:
                if qp in params:
                    if isinstance(params[qp], list):
                        if len(params[qp]) == 0:
                            query_string.append("{}=".format(qp))
                        else:
                            for val in params[qp]:
                                query_string.append("{}={}".format(qp, val))
                    else:
                        query_string.append("{}={}".format(qp, params[qp]))
            if len(query_string) > 0:
                final_url = final_url + "?" + "&".join(query_string)
        return final_url


class Traverson:
    """
    Traverson object to conveniently navigate in a HAL+JSON api
    """

    def __init__(self, base_url, jwt=None):
        """
        Construct an instance of the traverson
        :param base_url: the base url for the traverson
        :param jwt: a JSON Web Token to use during navigation
        """

        self.__session = Utils.get_hal_session(jwt)
        self.__base_url = base_url
        self.__hops = []

    def follow(self, link, params=None):
        """
        The link to follow from the current traverson state
        :param link: the name of the link
        :param params: the params to use for the link
        :return: the traverson
        """
        hop = {"link": link, "params": params}
        self.__hops.append(hop)
        return self

    def get(self):
        """
        Method to get the final result for the traverson
        :return: the content of the final destination
        """
        curr_url = self.__base_url
        logging.debug("Getting url {}".format(curr_url))
        response = self.__session.get(url=curr_url)
        if not is_ok(response):
            raise Exception("An error occurred while retrieving {} - HTTP({})".format(curr_url,
                                                                                      response.status_code))
        content = response.json()
        for hop in self.__hops:
            link = hop["link"]
            if content["_links"][link]:
                curr_url = content["_links"][link]["href"]
                # if hop["params"] is not None:
                if "templated" in content["_links"][link]:
                    curr_url = Utils.populate_url(curr_url, hop["params"])
                logging.debug("Getting url {}".format(curr_url))
                response = self.__session.get(url=curr_url)
                if not is_ok(response):
                    raise Exception("An error occurred while retrieving {} - HTTP({})".format(curr_url,
                                                                                              response.status_code),
                                    response)
                content = response.json()
            else:
                raise Exception("Couldn't find link {} on resource at {}".format(link, curr_url))
        return response


class SampleSearchResultsPageNavigator:
    """
    Object to navigate the search results using pagination links. This method does not guarantee
    the uniqueness of the results
    """

    def __init__(self, page):
        self.first_page = page
        self.session = Utils.get_hal_session()
        self.total_elements = page['page']['totalElements'] - page['page']['number'] * page['page'][
            'size']
        self._update_status(page)

    def _update_status(self, page_content):
        self.page_content = page_content['_embedded']['samples']
        self.page_metadata = page_content['page']
        self.links = page_content['_links']

    def get_all_results(self):
        """ Return all samples associated to the search"""
        while 'next' in self.links:
            for entry in self.page_content:
                yield entry

            next_link = self.links['next']['href']
            next_page_response = self.session.get(next_link)
            if is_ok(next_page_response):
                self._update_status(next_page_response.json())
            else:
                next_page_response.raise_for_status()

        for entry in self.page_content:
            yield entry

    def count(self):
        return self.total_elements


class SampleSearchResultsCursor:
    """
    Object to navigate biosamples search results using a cursor. If a cursor is not available, an exception
    is raised. This method guarantees the uniqueness of the results
    """

    def __init__(self, page):
        if 'cursor' not in page['_links']:
            raise Exception("The search results don't contain a cursor")
        self.session = Utils.get_hal_session()
        response = self.session.get(page['_links']['cursor']['href'])
        if is_ok(response):
            self.total_elements = page['page']['totalElements']
            cursor_page = response.json()
            self._update_status(cursor_page)
        else:
            response.raise_for_status()

    def _update_status(self, page):
        if '_embedded' not in page:
            self.page_content = []
            self.links = {}
            return
        self.page_content = page['_embedded']['samples']
        self.links = page['_links']

    def get_all_results(self):
        """ Return all samples associated to the search"""
        while 'next' in self.links:
            for entry in self.page_content:
                yield entry

            next_link = self.links['next']['href']
            next_page_response = self.session.get(next_link)
            if is_ok(next_page_response):
                self._update_status(next_page_response.json())
            else:
                next_page_response.raise_for_status()

        for entry in self.page_content:
            yield entry

    def count(self):
        return self.total_elements
