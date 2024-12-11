from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project

# Dynamically get the custom user model
User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'project_description', 'user']

    # Use the dynamically fetched user model
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)




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


