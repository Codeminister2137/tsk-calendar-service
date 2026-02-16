from rest_framework import serializers


class EnumField(serializers.ChoiceField):
    """
    A DRF serializer field for working with Python Enums.

    Converts between enum values and their string representations for both
    input validation and output serialization. Designed to be used with enums
    like `Priority` or `Status`.

    Args:
        enum_class (Enum): The Python Enum class to bind to the field.
        **kwargs (Any): Additional keyword arguments passed to `ChoiceField`.

    Methods:
        to_internal_value(data): Converts incoming value (str/int) to Enum instance.
        to_representation(obj): Converts Enum instance to its `.value` for output.

    Examples:
        >>> class ExampleSerializer(serializers.Serializer):
        ...     priority = EnumField(enum_class=Priority)
        >>> data = {"priority": "HIGH"}
        >>> serializer = ExampleSerializer(data=data)
        >>> serializer.is_valid()
        True
        >>> serializer.validated_data["priority"]
        <Priority.HIGH: 3>
        >>> serializer.data
        {'priority': 3}
    """

    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        super().__init__([(e.value, e.name) for e in enum_class], **kwargs)

    def to_internal_value(self, data):
        """
        Convert an incoming primitive value into the corresponding Enum member.

        Args:
            data (Any): The value received in the incoming request (e.g., form or JSON data).

        Returns:
            Enum (Enum): The corresponding Enum instance (e.g., Priority.HIGH).

        Raises:
            ValidationError: If the input value is not a valid choice.

        Examples:
            >>> field = EnumField(enum_class=Status)
            >>> field.to_internal_value("TODO")
            <Status.TODO: 'TODO'>
        """
        value = super().to_internal_value(data)
        return self.enum_class(value)

    def to_representation(self, obj):
        """
        Convert an Enum member into its primitive value for JSON output.

        Args:
            obj (Enum): The Enum instance to serialize.

        Returns:
            Any (str): The `.value` of the Enum (e.g., int or str), used in serialized output.

        Examples:
            >>> from calendar_app.enums import Priority
            >>> field = EnumField(enum_class=Priority)
            >>> field.to_representation(Priority.HIGH)
            3
        """
        return obj.value
