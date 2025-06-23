from rest_framework import serializers


class EnumField(serializers.ChoiceField):
    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        super().__init__([(e.value, e.name) for e in enum_class], **kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return self.enum_class(value)

    def to_representation(self, obj):
        return obj.value
