class JWTMissingException(Exception):
    pass


class ConvertionException(Exception):
    pass


class SampleConvertionException(ConvertionException):
    pass


class AttributeConvertionException(ConvertionException):
    pass


class RelationshipConvertionException(ConvertionException):
    pass
