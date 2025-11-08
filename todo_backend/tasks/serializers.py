"""
Task serializers for task management.
"""
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'user', 'user_email', 'title', 'description', 'category', 'priority',
            'is_completed', 'completed_at', 'due_date', 'reminder_time',
            'is_overdue', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'completed_at', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BulkTaskCreateSerializer(serializers.Serializer):
    """Serializer for bulk task creation"""
    tasks = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
        max_length=100  # Limit bulk operations
    )

    def validate_tasks(self, value):
        """Validate each task in the list"""
        for task_data in value:
            serializer = TaskSerializer(data=task_data, context=self.context)
            serializer.is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        tasks = []
        for task_data in validated_data['tasks']:
            task_data['user'] = user
            tasks.append(Task(**task_data))

        created_tasks = Task.objects.bulk_create(tasks)
        return created_tasks


class BulkTaskActionSerializer(serializers.Serializer):
    """Serializer for bulk task actions (delete, complete)"""
    task_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        max_length=100
    )
