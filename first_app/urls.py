from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path('hello/', views.hello_name, name='hello_name'),
    # path('first/', views.first_view, name='first_view'),
    # path('second/', views.second_view, name='second_view'),
    path('tasks/', tasks_create, name='tasks-create-list'),
    path('tasks/filter/', tasks_by_status_and_deadline, name='tasks-filter'),
    path('tasks/stats/', tasks_statistics, name='tasks-stats'),
    path('subtasks/create/', SubTaskCreateAPIView.as_view(), name='subtasks-create'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
