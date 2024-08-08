from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project: {self.title}"


class Task(models.Model):
    STATUSES_CHOICES = [
        ('New', 'New'),
        ('In_progress', 'In_progress'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    ]
    title = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(10)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUSES_CHOICES, default='New', max_length=15)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=15)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='tasks', blank=True)  # Удален 'null=True'
    due_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title
