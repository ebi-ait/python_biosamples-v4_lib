class _BioSamplesFilter:
    def __init__(self, filter_type):
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
        if not isinstance(value, str):
            raise Exception("Value must be a string")
        self.value = value
        return self


class _PredefinedFieldBioSamplesFilter(_BioSamplesFilter):
    def __init__(self, filter_type, target_field):
        super().__init__(filter_type=filter_type)
        self.field = target_field


class _NotPredefinedFieldBioSamplesFilter(_BioSamplesFilter):
    def __init__(self, filter_type):
        super().__init__(filter_type=filter_type)

    def with_target_field(self, target_field):
        if not isinstance(target_field, str):
            raise Exception("Targeted field must be a string")
        self.field = target_field
        return self


class AccessionFilter(_PredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("acc", None)


class NameFilter(_PredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("name", None)


class AttributeFilter(_NotPredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("attr")


class UpdateDateFilter(_PredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("dt", "update")


class ReleaseDateFilter(_PredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("dt", "release")


class RelationFilter(_NotPredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("rel")


class ReverseRelationFilter(_NotPredefinedFieldBioSamplesFilter):
    def __init__(self):
        super().__init__("rrel")
