import json
from datetime import datetime


class Sample:
    def __init__(self, accession=None, name=None, release=datetime.utcnow(), update=datetime.utcnow(),
                 attributes=None, relationships=None, external_references=None, organizations=None, contacts=None,
                 publications=None, domain=None, **kwargs):
        self.accession = accession
        self.name = name
        self.release = release
        self.update = update
        self.domain = domain
        if attributes is None:
            attributes = []
        self.attributes = []

        for crt_name in attributes:
            if isinstance(crt_name, Attribute):
                self.attributes.append(crt_name)
            else:
                crt_values = attributes[crt_name]
                for crt in crt_values:
                    self.attributes.append(
                        Attribute(name=crt_name, **crt))

        if relationships is None:
            relationships = []
        self.relations = relationships

        if external_references is None:
            external_references = []
        self.external_references = external_references

        if organizations is None:
            organizations = []
        self.organizations = organizations

        if contacts is None:
            contacts = []
        self.contacts = contacts

        if publications is None:
            publications = []
        self.publications = publications


    # @property
    # def accession(self):
    #     return self._accession
    #
    # @property
    # def name(self):
    #     return self._name
    #
    # @property
    # def release(self):
    #     return self._release
    #
    # @property
    # def update(self):
    #     return self._update
    #
    # @property
    # def characteristics(self):
    #     return self._characteristics
    #
    # @property
    # def relations(self):
    #     return self._relations
    #
    # @property
    # def external_references(self):
    #     return self._external_references
    #
    # @property
    # def organizations(self):
    #     return self._organizations
    #
    # @property
    # def contacts(self):
    #     return self._contacts
    #
    # @property
    # def publications(self):
    #     return self._publications
    #
    # @property
    # def domain(self):
    #     return self._domain

    def __str__(self):
        return "Sample {}".format(self.accession)


class Attribute:
    def __init__(self, name=None, value=None, iris=None, unit=None):
        if name is None or value is None:
            raise Exception("Attribute need at least a type and a value")
        self.name = name
        self.value = value
        if iris is None:
            iris = []
        self.iris = iris
        self.unit = unit

    # @property
    # def name(self):
    #     return self._name
    #
    # @property
    # def value(self):
    #     return self._value
    #
    # @property
    # def iris(self):
    #     return self._iris
    #
    # @property
    # def unit(self):
    #     return self._unit


class Relationship:
    def __init__(self, source=None, type=None, target=None):
        if source is None or type is None or target is None:
            raise Exception("You need to provide a source, "
                            "a target and the type of relation to make it valid")
        self._source = source
        self._type = type
        self._target = target

    @property
    def source(self):
        return self._source

    @property
    def type(self):
        return self._type

    @property
    def target(self):
        return self._target