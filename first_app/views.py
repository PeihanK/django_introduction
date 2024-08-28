from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer


# Create your views here.

# def hello_name(request):
#     name = 'Konstantin'
#     return HttpResponse(
#         f"<h1 style='color: #f4ce14; background-color: #495e57; text-align: center;'>Hello, {name}</h1>")
#
#
# def first_view(request):
#     return HttpResponse("<h1>Hello, world. You're at the polls view.</h1>")
#
#
# def second_view(request):
#     return HttpResponse("<h1>Hello, world. It's second view.</h1>")


@api_view(['POST', 'GET'])
def tasks_create(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tasks_by_status_and_deadline(request):
    status_filter = request.query_params.get('status')
    deadline_filter = request.query_params.get('deadline')

    tasks = Task.objects.all()

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if deadline_filter:
        tasks = tasks.filter(deadline__lte=deadline_filter)

    paginator = PageNumberPagination()
    paginator.page_size = 3
    paginated_tasks = paginator.paginate_queryset(tasks, request)

    serializer = TaskSerializer(paginated_tasks, many=True)
    return paginator.get_paginated_response(serializer.data)


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


class SubTaskCreateAPIView(generics.CreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)


    def put(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

