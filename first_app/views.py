from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics, status, filters, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, SubTask, Category
from .serializers import TaskSerializer, SubTaskCreateSerializer, CategoryCreateSerializer


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = 'created_at'


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubTaskList(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = 'created_at'


class SubTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=True, methods=['GET'])
    def count_tasks(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            task_count = category.tasks.count()

            data = {
                "id": category.id,
                "category": category.name,
                "task_count": task_count
            }

            return Response(data)

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def tasks_statistics(request):
    total_tasks = Task.objects.count()
    count_by_status = Task.objects.values('status').annotate(count=Count('id'))
    overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()

    response_data = {
        'total_tasks': total_tasks,
        'status_count': count_by_status,
        'overdue_tasks': overdue_tasks
    }

    return Response(response_data)
