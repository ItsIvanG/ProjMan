from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound

from .forms import CreateUserForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Report
from .serializers import ProjectSerializer, ReportSerializer
from django.shortcuts import get_object_or_404



@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})


@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        password = data['password']
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON'}, status=400
        )

    user = authenticate(request, username=email, password=password)

    if user:
        login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse(
        {'success': False, 'message': 'Invalid credentials'}, status=401
    )


def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})


@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        user_data = {
            'id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'role': request.user.role, 
            'is_active': request.user.is_active,
            'manager_id': request.user.manager_id,
        }
        return JsonResponse(user_data)
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )


@require_http_methods(['POST'])
def register(request):

    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)
    
class ProjectCreateView(APIView):
    def get(self, request, manager_id=None):
        if manager_id:
            # Filter projects by the manager_id (plain IntegerField)
            projects = Project.objects.filter(manager_id=manager_id,archived=False)
        else:
            # If no manager_id is provided, return all projects
            projects = Project.objects.all()

        # Serialize the projects and return them
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id=None):
        if not project_id:
            return Response({"error": "Project ID is required for updating."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the project object or return a 404 if it doesn't exist
        project = get_object_or_404(Project, project_id=project_id)

        # Pass the existing project instance and new data to the serializer
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the updated instance
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArchiveProjectView(APIView):
    def get(self, request, manager_id=None):
        if manager_id:
            # Filter projects by the manager_id (plain IntegerField)
            projects = Project.objects.filter(manager_id=manager_id, archived=True)
        else:
            # If no manager_id is provided, return all projects
            projects = Project.objects.all()

        # Serialize the projects and return them
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id=None):
        if not project_id:
            return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the project by ID or return a 404 error if not found
        project = get_object_or_404(Project, project_id=project_id)

        # Update the 'archived' status to True
        project.archived = True
        project.save()
        print(str(project_id) + " archived")
        return Response(
            {
                "message": f"Project '{project.project_name}' has been archived.",
                "project_id": project.project_id,
                "archived": project.archived,
            },
            status=status.HTTP_200_OK
        )

class UnarchiveProjectView(APIView):
    def post(self, request, project_id=None):
        if not project_id:
            return Response({"error": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the project by ID or return a 404 error if not found
        project = get_object_or_404(Project, project_id=project_id)

        # Update the 'archived' status to True
        project.archived = False
        project.save()
        print(str(project_id) + " unarchived")
        return Response(
            {
                "message": f"Project '{project.project_name}' has been unarchived.",
                "project_id": project.project_id,
                "archived": project.archived,
            },
            status=status.HTTP_200_OK
        )

from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Get the project_id from URL parameters
        project_id = self.kwargs['project_id']
        # Get the status from query parameters, if present
        status = self.request.query_params.get('status', None)

        # Filter tasks by project_id
        queryset = Task.objects.filter(project_id=project_id)

        # Optionally filter by status
        if status:
            queryset = queryset.filter(status=status)

        # Sort by sprint (ascending by default)
        queryset = queryset.order_by('sprint')

        return queryset

        
    
class TaskEditView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Overriding the get_object method to fetch the task by ID
    def get_object(self):
        task_id = self.kwargs['task_id']  # Get task_id from URL parameters
        return Task.objects.get(task_id=task_id)  # Fetch the task by ID

from .serializers import AssignTaskSerializer
    
class TaskAssignEditView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = AssignTaskSerializer

    # Overriding the get_object method to fetch the task by ID
    def get_object(self):
        task_id = self.kwargs['task_id']  # Get task_id from URL parameters
        return Task.objects.get(task_id=task_id)  # Fetch the task by ID


from .models import User
from .serializers import UserSerializer

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        manager_id = self.kwargs.get('manager_id')
        is_active = self.request.query_params.get('is_active', None)  # Get the is_active filter from query parameters

        queryset = User.objects.filter(manager_id=manager_id)

        if is_active is not None:
            is_active = bool(int(is_active))  # Convert the value to a boolean
            queryset = queryset.filter(is_active=is_active)

        return queryset
    

from .serializers import UserCreateSerializer

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


from .serializers import UserUpdateSerializer 

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


from rest_framework import generics
from .serializers import UserIsActiveUpdateSerializer
from .models import User

class UserIsActiveUpdateView(generics.UpdateAPIView):
    serializer_class = UserIsActiveUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        # Fetch the user object based on the ID in the URL
        return self.get_queryset().get(id=self.kwargs['pk'])


class ReportListCreateAPIView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportUpdateAPIView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_object(self):
        try:
            return Report.objects.get(report_id=self.kwargs['report_id'])
        except Report.DoesNotExist:
            raise NotFound(detail="Report not found.")

    def perform_update(self, serializer):
        # Optionally associate with logged-in user
        # serializer.save(user=self.request.user)
        serializer.save()

from rest_framework import generics
from .models import File
from .serializers import FileSerializer

class FileCreateAPIView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    

class FileListByProjectAPIView(generics.ListAPIView):
    """
    API view to list all files associated with a specific project ID.
    """
    serializer_class = FileSerializer

    def get_queryset(self):
        # Get the project ID from the URL query parameters
        project_id = self.kwargs['project_id']
        return File.objects.filter(project_id=project_id)

