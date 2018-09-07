class _BioSamplesFilter:
    """
    Base class for BioSamples filters
    """

    def __init__(self, filter_type):
        """
        Constructor
        :param filter_type: the type of the filter
        """
        self.filter_type = filter_type
        self.field = None
        self.value = None

    def get_type(self):
        return self.filter_type

    def get_target_field(self):
        return self.field

    def get_value(self):
        return self.value

    def with_value(self, value):
        """
        Setter for the value of the filter
        :param value: the value to filter
        :type value: string
        :return: the filter itself
        """
        if not isinstance(value, str):
            raise Exception("Value must be a string")
        self.value = value
        return self


class _PredefinedFieldBioSamplesFilter(_BioSamplesFilter):
    """
    Base class for those filters in BioSamples with a predefined target field
    """

    def __init__(self, filter_type, target_field):
        super().__init__(filter_type=filter_type)
        self.field = target_field


class _NotPredefinedFieldBioSamplesFilter(_BioSamplesFilter):
    """
    Base class for filters in BioSamples without a predefined target field
    """

    def __init__(self, filter_type):
        super().__init__(filter_type=filter_type)

    def with_target_field(self, target_field):
        """
        Setter of the target field for the filter
        :param target_field: the field to use for the filter
        :type target_field: str
        :return: the filter itself
        """
        if not isinstance(target_field, str):
            raise Exception("Targeted field must be a string")
        self.field = target_field
        return self


class AccessionFilter(_PredefinedFieldBioSamplesFilter):
    """
    Filter samples by accession
    """

    def __init__(self):
        super().__init__("acc", None)


class NameFilter(_PredefinedFieldBioSamplesFilter):
    """
    Filter samples by name
    """

    def __init__(self):
        super().__init__("name", None)


class AttributeFilter(_NotPredefinedFieldBioSamplesFilter):
    """
    Filter samples by Attribute
    """

    def __init__(self):
        super().__init__("attr")


class UpdateDateFilter(_PredefinedFieldBioSamplesFilter):
    """
    Filter samples by update date
    """

    def __init__(self):
        super().__init__("dt", "update")


class ReleaseDateFilter(_PredefinedFieldBioSamplesFilter):
    """
    Filter samples by release date
    """

    def __init__(self):
        super().__init__("dt", "release")


class RelationFilter(_NotPredefinedFieldBioSamplesFilter):
    """
    Filter samples by relation
    """

    def __init__(self):
        super().__init__("rel")


class ReverseRelationFilter(_NotPredefinedFieldBioSamplesFilter):
    """
    Filter samples by inverse relation
    """

    def __init__(self):
        super().__init__("rrel")


class DomainFilter(_PredefinedFieldBioSamplesFilter):
    """
    Filter samples by domain
    """

    def __init__(self):
        super().__init__("dom", None)
