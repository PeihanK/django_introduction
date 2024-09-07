from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('tasks/', TaskList.as_view(), name='tasks-create-list'),
    path('tasks/filter/', TaskList.as_view(), name='tasks-filter'),
    path('tasks/stats/', tasks_statistics, name='tasks-stats'),
    path('subtasks/', SubTaskList.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetail.as_view(), name='subtask-detail-update-delete'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', include(router.urls)),


]
