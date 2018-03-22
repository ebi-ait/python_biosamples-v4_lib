from .exceptions import *


def dict_to_sample(d):
    """
    Try to convert a dictionary to a sample
    :param d: dictionarty to convert
    :return: a sample
    """
    try:
        accession = d['accession']
        attrs = d['characteristics']
        relationships = getattr(d, 'rel')
    except Exception:
        raise SampleConvertionException()


def dict_to_attribute(d):
    """
    Try to convert a dictionary to the corrispondent attribute
    :param d: dictionary to convert
    :return: an attribute
    """
    raise AttributeConvertionException()


def dict_to_relationship(d):
    """
    Try to convert a dictionary to a relationship object
    :param d:
    :return:
    """
    raise RelationshipConvertionException()


def dict_to_curation(d):
    pass


def dict_to_curation_link(d):
    pass