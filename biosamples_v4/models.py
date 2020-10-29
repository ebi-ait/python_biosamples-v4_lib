import logging
from datetime import datetime
from .filters import _BioSamplesFilter
from .utilities import ena_json_response
import requests
from urllib.parse import quote
import json


class Sample:
    def __init__(self, sample=None, accession=None, name=None, release=datetime.utcnow(), update=datetime.utcnow(),
                 attributes=None, relationships=None, external_references=None, organizations=None, contacts=None,
                 publications=None, domain=None, species=None, ncbi_taxon_id=None):
        self.sample = sample
        self.accession = accession
        self.name = name
        self.release = release
        self.update = update
        self.domain = domain
        self.species = species
        self.ncbi_taxon_id = str(ncbi_taxon_id) if ncbi_taxon_id is not None else ncbi_taxon_id
        self.attributes = [] if attributes is None else attributes
        self.relations = [] if relationships is None else relationships
        self.external_references = [] if external_references is None else external_references
        self.organizations = [] if organizations is None else organizations
        self.contacts = [] if contacts is None else contacts
        self.publications = [] if publications is None else publications

        self._store_organism_info()

    def __str__(self):
        return "Sample {}".format(self.accession)

    def _store_organism_info(self):
        ena_species_lookup_base = "http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/scientific-name/"
        ena_taxid_lookup_base = "http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/tax-id/"
        if self.species is not None and self.ncbi_taxon_id is None:
            self.species = self.species.capitalize()
            response = requests.get(ena_species_lookup_base + quote(self.species))
            response_json = ena_json_response(response)
            if isinstance(response_json, list):
                response_json = response_json[0]
            print("Found taxon for species " + self.species + " with ncbi taxon id " + response_json["taxId"])
            self.ncbi_taxon_id = response_json["taxId"]
        elif self.species is None and self.ncbi_taxon_id is not None:
            response = requests.get(ena_taxid_lookup_base + quote(self.ncbi_taxon_id))
            response_json = ena_json_response(response)
            if isinstance(response_json, list):
                response_json = response_json[0]
            print("Found species for taxon " + self.ncbi_taxon_id + " with species " + response_json["scientificName"])
            self.species = response_json["scientificName"]
        elif self.species is not None and self.ncbi_taxon_id is not None:
            self.species = self.species.capitalize()
            species_response = requests.get(ena_species_lookup_base + quote(self.species))
            species_response_json = ena_json_response(species_response)
            if isinstance(species_response_json, list):
                species_response_json = species_response_json[0]
            taxid_response = requests.get(ena_taxid_lookup_base + quote(self.ncbi_taxon_id))
            taxid_response_json = ena_json_response(taxid_response)
            if isinstance(taxid_response_json, list):
                taxid_response_json = taxid_response_json[0]
            if species_response_json["taxId"] != str(self.ncbi_taxon_id):
                print("Information is not consistent between " + self.species + " and " + str(self.ncbi_taxon_id))
            if taxid_response_json["scientificName"] != self.species:
                print("Information is not consistent between " + self.species + " and " + str(self.ncbi_taxon_id) +
                      ". Please check information and re-run method")
        else:
            print("Without either species or ncbi_taxon_id cannot determine organism info, please set one of these")


    def _append_organism_attribute(self):
        if self.species is not None and self.ncbi_taxon_id is not None:
            self.attributes.append(Attribute(name="organism",
                                             value=self.species,
                                             iris="http://purl.obolibrary.org/obo/NCBITaxon_" + self.ncbi_taxon_id))




class Attribute:
    # TODO: make sure if list of iris supplied still 1d list of iris is returned
    def __init__(self, name=None, value=None, iris=None, unit=None):
        if name is None or value is None:
            raise Exception("Attribute need at least a type and a value")
        self.name = name
        self.value = value
        self.iris = [] if iris is None else [iris]
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
