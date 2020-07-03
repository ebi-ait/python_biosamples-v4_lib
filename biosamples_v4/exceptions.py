class JWTMissingException(Exception):
    pass


class ConversionException(Exception):
    pass


class SampleConversionException(ConversionException):
    pass


class AttributeConversionException(ConversionException):
    pass


class RelationshipConversionException(ConversionException):
    pass


class OrganismInformationIncompleteException(Exception):
    pass
