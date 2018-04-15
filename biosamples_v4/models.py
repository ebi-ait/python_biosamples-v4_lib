import logging
from datetime import datetime
from .filters import _BioSamplesFilter


class Sample:
    def __init__(self, sample=None, accession=None, name=None, release=datetime.utcnow(), update=datetime.utcnow(),
                 attributes=None, relationships=None, external_references=None, organizations=None, contacts=None,
                 publications=None, domain=None):
        self.sample = sample
        self.accession = accession
        self.name = name
        self.release = release
        self.update = update
        self.domain = domain
        self.attributes = [] if attributes is None else attributes
        self.relations = [] if relationships is None else relationships
        self.external_references = [] if external_references is None else external_references
        self.organizations = [] if organizations is None else organizations
        self.contacts = [] if contacts is None else contacts
        self.publications = [] if publications is None else publications

    def __str__(self):
        return "Sample {}".format(self.accession)


class Attribute:
    def __init__(self, name=None, value=None, iris=None, unit=None):
        if name is None or value is None:
            raise Exception("Attribute need at least a type and a value")
        self.name = name
        self.value = value
        self.iris = [] if iris is None else iris
        self.unit = unit


class Relationship:
    def __init__(self, source=None, rel_type=None, target=None):
        if source is None or rel_type is None or target is None:
            raise Exception("You need to provide a source, "
                            "a target and the rel_type of relation to make it valid")
        self.source = source
        self.rel_type = type
        self.target = target


class Curation:
    def __init__(self, attributes_pre=None, attributes_post=None,
                 external_references_pre=None, external_references_post=None):
        self.attr_pre = [] if attributes_pre is None else attributes_pre
        self.attr_post = [] if attributes_post is None else attributes_post
        self.rel_pre = [] if external_references_pre is None else external_references_pre
        self.rel_post = [] if external_references_post is None else external_references_post


class CurationLink:
    def __init__(self, accession=None, curation=None, domain=None):

        if accession is None:
            raise Exception("An accession is needed to create a curation link")

        if curation is None or type(curation) is not Curation:
            raise Exception("You need to provide a curation object as part of a curation link")

        if domain is None:
            raise Exception("You need to provide a domain with the curation link")

        self.accession = accession
        self.curation = curation
        self.domain = domain


class SearchQuery:
    def __init__(self, text=None, filters=None, page=0, size=20):
        self.text = text
        self.filters = list()
        if filters is not None:
            if isinstance(filters, _BioSamplesFilter):
                self.filters.append(filters)
            else:
                if not hasattr(filters, '__iter__'):
                    raise Exception("Provided object is not iterable")
                for f in filters:
                    if not isinstance(f, _BioSamplesFilter):
                        raise Exception("Provided object {} is not a BioSamplesFilter".format(f))
                    self.filters.append(f)
        self.page = page
        self.size = size
