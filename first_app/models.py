from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ['name']


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(help_text='Task name', max_length=255)
    description = models.TextField(help_text='Task description', null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ['title']


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ['title']
