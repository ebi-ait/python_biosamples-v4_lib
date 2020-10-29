class JWTMissingException(Exception):
    pass


class CursorNotFoundException(KeyError):
    pass


class LinkNotFoundException(KeyError):
    pass


class ConvertionException(Exception):
    pass


class SampleConvertionException(ConvertionException):
    pass


class AttributeConvertionException(ConvertionException):
    pass


class RelationshipConvertionException(ConvertionException):
    pass
