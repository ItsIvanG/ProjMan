from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project

# Dynamically get the custom user model
User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'project_description', 'user', 'manager_id']





from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    task_id = serializers.ReadOnlyField()
    task_code = serializers.ReadOnlyField()
    assignee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['task_id', 'task_code', 'features', 'status', 'assignee', 'sprint', 'priority', 'deadline', 'project']

    def get_assignee(self, obj):
        # Assuming 'username' is the field you want to show from the assignee (user model)
        return obj.assignee.name if obj.assignee else None
    
class AssignTaskSerializer(serializers.ModelSerializer):
    task_id = serializers.ReadOnlyField()
    task_code = serializers.ReadOnlyField()
    assignee = serializers.SerializerMethodField()
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Replace `User` with the appropriate model for your assignees
        source='assignee',
        write_only=True
    )

    class Meta:
        model = Task
        fields = ['task_id', 'task_code', 'features', 'status', 'assignee', 'assignee_id', 'sprint', 'priority', 'deadline', 'project']
        read_only_fields = ['task_id', 'task_code', 'features', 'status', 'assignee', 'sprint', 'priority', 'deadline', 'project']

    def get_assignee(self, obj):
        # Assuming 'name' is the field you want to show from the assignee (user model)
        return obj.assignee.name if obj.assignee else None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'role', 'manager', 'is_active']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'role', 'manager', 'is_active', 'password']

    def create(self, validated_data):
        # Hash the password before saving the user
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'role', 'manager', 'is_active', 'password']

    def update(self, instance, validated_data):
        # If a new password is provided, hash it and update
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

from rest_framework import serializers
from .models import User

class UserIsActiveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_active']

    def update(self, instance, validated_data):
        # Only update the is_active field
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
