import json
import re
import requests
from requests.exceptions import HTTPError

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def clean_json(json):
    new_json = json
    if isinstance(new_json, dict):
        new_json.pop("_links")
    return new_json


def merge_samples(sample_a, sample_b):
    if sample_a["accession"] != sample_b["accession"]:
        raise Exception("Impossible to merge samples with different accessions")
    return {**clean_json(sample_a), **clean_json(sample_b)}


def is_ok(response):
    return response.status_code == requests.codes['ok']


def is_not_found(response):
    return response.status_code == requests.codes['not_found']


def is_successful(response):
    return 200 <= response.status_code < 300


def is_status(response, code=None):
    if code is None:
        raise ValueError("No code has been provided to the function")
    if isinstance(code, list):
        return response.status_code in code
    return response.status_code == code


def ena_json_response(response):
    if response.text == 'No results.':
        raise HTTPError(f'404 Client Error: No Results at: {response.url}', response)
    return json.loads(response.content)


def raise_error_with_reason(response):
    if is_not_found(response):
        response.reason = 'No Results'
    try:
        response.reason = response.json()['message']
    except (KeyError, ValueError):
        pass

    raise response.raise_for_status()
