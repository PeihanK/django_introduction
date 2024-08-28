from django.utils import timezone
from rest_framework import serializers
from .models import Task, SubTask, Category


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at']

        def validate_deadline(self, value):
            if value < timezone.now():
                raise serializers.ValidationError('Deadline cannot be in past')
            return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'task', 'description', 'deadline', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

        def create(self, validated_data):
            name = validated_data.pop('name')

            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError({'name': 'Category already exists'})

            return Category.objects.create(name=name)

        def update(self, instance, validated_data):
            name = validated_data.get('name', instance.name)
            if Category.objects.filter(name=name).exclude(id=instance.id).exists():
                raise serializers.ValidationError({'name': 'Category already exists'})

            instance.name = name
            return instance
