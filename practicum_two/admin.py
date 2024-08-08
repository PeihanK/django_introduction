from django.contrib import admin
from .models import Project, Task, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'created_at', 'due_date')
    search_fields = ('title',)
    list_filter = ('status', 'priority', 'project', 'created_at', 'due_date')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
