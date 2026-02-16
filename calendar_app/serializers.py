from rest_framework import serializers

from calendar_app.enums import Priority, Status
from calendar_app.fields import EnumField


class TaskJsonInputSerializer(serializers.Serializer):
    """
    Serializer for validating and deserializing JSON input when creating or updating a Task.

    Attributes:
        name (str): Required. The name/title of the task (max length 255).
        expected_duration (timedelta): Optional. Estimated time to complete the task.
        actual_duration (timedelta): Optional. Time actually spent on the task.
        categories (List[str]): Optional. List of category labels associated with the task.
        deadline (datetime): Optional. Deadline date and time.
        priority (Priority): Optional. Enum value representing task priority.
        notifications (List[Any]): Optional. List of datetime objects indicating when to send notifications.
        status (Status): Optional. Enum value representing current task status.

    Examples:
        >>> data = {
        ...     "name": "Write report",
        ...     "expected_duration": "02:00:00",
        ...     "categories": ["work", "writing"],
        ...     "deadline": "2025-07-21T17:00:00Z",
        ...     "priority": "HIGH",
        ...     "status": "TODO"
        ... }
        >>> serializer = TaskJsonInputSerializer(data=data)
        >>> serializer.is_valid()
        True
        >>> serializer.validated_data["priority"]
        <Priority.HIGH: 3>
    """

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
