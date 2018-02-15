import re
import requests


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def clean_json(json):
    new_json = json
    if isinstance(new_json, dict):
        new_json.pop("_links")
    return new_json


def merge_samples(sampleA, sampleB):
    if sampleA["accession"] != sampleB["accession"]:
        raise Exception("Impossible to merge samples with different accessions")
    return {**clean_json(sampleA), **clean_json(sampleB)}


def is_ok(response):
    return response.status_code == requests.codes.ok
