from rest_framework import serializers

from calendar_app.enums import Priority, Status


class TaskJsonInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    expected_duration = serializers.DurationField(required=False)
    actual_duration = serializers.DurationField(required=False)
    categories = serializers.ListField(required=False)
    deadline = serializers.DateTimeField(required=False)
    priority = serializers.ChoiceField(
        choices=[(priority.value, priority.name) for priority in Priority],
        required=False,
    )
    notifications = serializers.ListField(required=False)
    status = serializers.ChoiceField(
        choices=[(status.value, status.name) for status in Status], required=False
    )
