from rest_framework import serializers

from calendar_app.enums import Priority, Status
from calendar_app.fields import EnumField


class TaskJsonInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    expected_duration = serializers.DurationField(required=False)
    actual_duration = serializers.DurationField(required=False)
    categories = serializers.ListField(required=False)
    deadline = serializers.DateTimeField(required=False)
    priority = EnumField(
        Priority,
        required=False,
    )
    notifications = serializers.ListField(required=False)
    status = EnumField(Status, required=False)
