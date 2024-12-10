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
