from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *


router = DefaultRouter()
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='tasks-create-list'),
    path('tasks/filter/', TaskDetail.as_view(), name='tasks-filter'),
    path('tasks/stats/', tasks_statistics, name='tasks-stats'),
    path('subtasks/', SubTaskList.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetail.as_view(), name='subtask-detail-update-delete'),
    path('', include(router.urls)),
]
