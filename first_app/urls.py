from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('hello/', views.hello_name, name='hello_name'),
    path('first/', views.first_view, name='first_view'),
    path('second/', views.second_view, name='second_view'),
    path('tasks/', views.tasks_create, name='tasks-create-list'),
    path('tasks/filter/', views.tasks_by_status_and_deadline, name='tasks-filter'),
    path('tasks/stats/', views.tasks_statistics, name='tasks-stats'),
]
