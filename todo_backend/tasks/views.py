"""
Task views for task management with bulk operations.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, BulkTaskCreateSerializer, BulkTaskActionSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for task CRUD operations"""
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'priority', 'is_completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return tasks for the current user, excluding soft-deleted"""
        return Task.objects.filter(
            user=self.request.user,
            deleted_at__isnull=True
        )

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a task as complete"""
        task = self.get_object()
        task.mark_complete()
        return Response({
            'message': 'Task marked as complete',
            'task': TaskSerializer(task).data
        })

    @action(detail=True, methods=['post'])
    def incomplete(self, request, pk=None):
        """Mark a task as incomplete"""
        task = self.get_object()
        task.mark_incomplete()
        return Response({
            'message': 'Task marked as incomplete',
            'task': TaskSerializer(task).data
        })

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create tasks"""
        serializer = BulkTaskCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        tasks = serializer.save()

        return Response({
            'message': f'{len(tasks)} tasks created successfully',
            'tasks': TaskSerializer(tasks, many=True).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Bulk delete tasks (soft delete)"""
        serializer = BulkTaskActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_ids = serializer.validated_data['task_ids']
        tasks = Task.objects.filter(
            id__in=task_ids,
            user=request.user,
            deleted_at__isnull=True
        )

        updated_count = tasks.update(deleted_at=timezone.now())

        return Response({
            'message': f'{updated_count} tasks deleted successfully',
            'deleted_count': updated_count
        })

    @action(detail=False, methods=['post'])
    def bulk_complete(self, request):
        """Bulk mark tasks as complete"""
        serializer = BulkTaskActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_ids = serializer.validated_data['task_ids']
        tasks = Task.objects.filter(
            id__in=task_ids,
            user=request.user,
            is_completed=False,
            deleted_at__isnull=True
        )

        updated_count = tasks.update(
            is_completed=True,
            completed_at=timezone.now()
        )

        return Response({
            'message': f'{updated_count} tasks marked as complete',
            'completed_count': updated_count
        })
