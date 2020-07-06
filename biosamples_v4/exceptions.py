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


class OrganismInformationIncompleteWarning(UserWarning):
    pass


class InvalidRelationshipException(Exception):
    pass
