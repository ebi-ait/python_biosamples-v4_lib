from urllib import parse as urlencoder
from json import JSONEncoder
from datetime import datetime
from .models import Sample, Attribute, Relationship, CurationLink, Curation, SearchQuery
from .filters import _BioSamplesFilter, _PredefinedFieldBioSamplesFilter


class ISODateTimeEncoder(JSONEncoder):
    """
    JSON encoder for ISO DateTimes in BioSamples
    """
    def default(self, o):
        if not isinstance(o, datetime):
            raise Exception("The provided object is not a datetime")
        return o.strftime("%Y-%m-%dT%H:%M:%SZ%z")


class SampleEncoder(JSONEncoder):
    """
    JSON encoder for samples
    """
    def default(self, o):
        if not isinstance(o, Sample):
            raise Exception("The provided object is not a Sample")

        attribute_list_encoder = AttributeListEncoder()
        relatioship_encoder = RelationshipEncoder()
        datetime_encoder = ISODateTimeEncoder()

        _dict = dict()
        _dict["accession"] = o.accession
        _dict["release"] = datetime_encoder.default(o.release)
        _dict["update"] = datetime_encoder.default(o.update)
        _dict["characteristics"] = attribute_list_encoder.default(o.attributes)
        _dict["relationships"] = [relatioship_encoder.default(rel) for rel in o.relations]
        _dict["externalReferences"] = o.external_references
        _dict["organization"] = o.organizations
        _dict["contact"] = o.contacts
        return _dict


class AttributeEncoder(JSONEncoder):
    """
    JSON encoder for Attributes
    """
    def default(self, o):
        if not isinstance(o, Attribute):
            raise Exception("The provided object is not an Attribute")

        _dict = dict()
        _dict["type"] = o.name
        _dict["text"] = o.value
        _dict["iri"] = o.iris
        _dict["unit"] = o.unit
        return _dict


class RelationshipEncoder(JSONEncoder):
    """
    JSON encoder for relationships
    """
    def default(self, o):
        if not isinstance(o, Relationship):
            raise Exception("The provided object is not a Relationship")

        _dict = dict()
        _dict["source"] = o.source
        _dict["type"] = o.type
        _dict["target"] = o.target


class AttributeListEncoder(JSONEncoder):
    """
    JSON encoder for attribute list
    """
    def default(self, o):

        if not isinstance(o, list):
            return JSONEncoder.default(self, o)

        attr_encoder = AttributeEncoder()
        _dict = dict()
        for attr in o:
            if not isinstance(attr, Attribute):
                raise Exception("The provided list contains a non attribute object")

            attr_dict = attr_encoder.default(attr)
            attr_dict.pop("type", None)
            _dict.setdefault(attr.name, []).append(attr_dict)

        return _dict


class ExternalReferenceEncoder(JSONEncoder):
    """
    JSON encoder for ExternalReferences
    """
    def default(self, o):
        _dict = {"url": o["url"]}
        return _dict


class CurationEncoder(JSONEncoder):
    """
    JSON encoder for Curation objects
    """
    def default(self, o):
        if not isinstance(o, Curation):
            return JSONEncoder.default(self, o)

        _dict = dict()
        _dict["attributesPre"] = o.attr_pre
        _dict["attributesPost"] = o.attr_post
        _dict["externalReferencesPre"] = o.rel_pre
        _dict["externalReferencesPost"] = o.rel_post
        return _dict


class CurationLinkEncoder(JSONEncoder):
    """
    JSON encoder for the CurationLink object
    """
    def default(self, o):
        if not isinstance(o, CurationLink):
            return JSONEncoder.default(self, o)

        _cur_encoder = CurationEncoder()
        _dict = dict()
        _dict["sample"] = o.accession
        _dict["curation"] = _cur_encoder.default(o.curation)
        _dict["domain"] = o.domain
        return _dict


class BiosamplesFilterEncoder(JSONEncoder):
    """
    Encoder for BioSamples filter
    """
    def default(self, o):
        if not isinstance(o, _BioSamplesFilter):
            return JSONEncoder.default(self, o)

        encoded_value = o.get_value()
        if isinstance(o, _PredefinedFieldBioSamplesFilter):
            return "{}:{}".format(o.get_type(), encoded_value)
        else:
            if o.get_target_field() is None:
                raise Exception("Error while encoding a not predefined target field filter")
            encoded_field = o.get_target_field()
            if encoded_value is None:
                return "{}:{}".format(o.get_type(), encoded_field)
            else:
                return "{}:{}:{}".format(o.get_type(), encoded_field, encoded_value)


class SearchQueryEncoder(JSONEncoder):
    """
    Encoder for the SearchQuery Object
    """
    def default(self, o):
        if not isinstance(o, SearchQuery):
            return JSONEncoder.default(o)

        _biosamples_filter_encoder = BiosamplesFilterEncoder()
        _dict = dict()
        if o.text is not None:
            _dict['text'] = o.text
        if o.filters is not None and len(o.filters) > 0:
            _dict['filter'] = [_biosamples_filter_encoder.default(f) for f in o.filters]
        _dict['page'] = o.page
        _dict['size'] = o.size
        return _dict
