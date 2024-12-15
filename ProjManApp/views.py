from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound,ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .forms import CreateUserForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Report
from .serializers import ProjectSerializer, ReportSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
import os
from django.conf import settings



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
            'username': request.user.username,
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

class FilterTasksAPIView(APIView):
    """
    API view to retrieve tasks by project_id, assignee_id,
    and status = 'In Progress' OR 'Not Started'.
    """
    def get(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('project_id')
        assignee_id = self.request.query_params.get('assignee_id')

        # Ensure parameters are provided
        if not project_id or not assignee_id:
            return Response(
                {"null"},
               status=status.HTTP_200_OK
            )

        try:
            tasks = Task.objects.filter(
                project_id=project_id,
                assignee_id=assignee_id
            ).filter(
                Q(status="In Progress") | Q(status="Not started")
            )
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskCompletionPercentageAPIView(APIView):
    """
    API view to get the percentage of tasks with status 'Completed'
    compared to tasks with non-completed status for a given project.
    """

    def get(self, request, *args, **kwargs):
        # Get the project_id from query params
        project_id = self.request.query_params.get('project_id')

        # Ensure the project_id is provided
        if not project_id:
            return Response(
                {"error": "project_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get the total number of tasks for the given project_id
            total_tasks = Task.objects.filter(project_id=project_id).count()

            # Count the tasks with status 'Completed' for the given project_id
            completed_tasks = Task.objects.filter(project_id=project_id, status="Completed").count()
            cancelled = Task.objects.filter(project_id=project_id, status="Cancelled").count()
            ongoing = Task.objects.filter(project_id=project_id, status="In Progress").count()
            not_started = Task.objects.filter(project_id=project_id, status="Not started").count()


            total_tasks -= cancelled
            # Calculate non-completed tasks
            non_completed_tasks = total_tasks - completed_tasks

            # Avoid division by zero
            if total_tasks == 0:
                data = {
                    "completed_percentage": 0,
                    "non_completed_percentage": 0,
                    "total_tasks": 0,
                    "completed": 0,
                    "ongoing": 0,
                    "not_started": 0,
                }

                return Response(data, status=status.HTTP_200_OK)
                # return Response(
                #     {"error": "No tasks available in this project to calculate percentages."},
                #     status=status.HTTP_400_BAD_REQUEST
                # )

            # Calculate the percentages
            completed_percentage = (completed_tasks / total_tasks) * 100
            non_completed_percentage = (non_completed_tasks / total_tasks) * 100

            # Prepare the response data
            data = {
                "completed_percentage": completed_percentage,
                "non_completed_percentage": non_completed_percentage,
                "total_tasks": total_tasks,
                "completed" : completed_tasks,
                "ongoing" : ongoing,
                "not_started": not_started,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# views.py

class ProjectDetailAPIView(APIView):
    """
    API view to retrieve a specific project by project_id.
    """

    def get(self, request, *args, **kwargs):
        # Get the project_id from the URL parameters
        project_id = kwargs.get('project_id')

        # Ensure the project_id is provided
        if not project_id:
            return Response(
                {"error": "project_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve the project with the given project_id
            project = Project.objects.get(project_id=project_id)

            # Serialize the project data
            serializer = ProjectSerializer(project)

            # Return the serialized project data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserByManagerAPIView(APIView):
    """
    API view to retrieve all users with a specific manager_id.
    """

    def get(self, request, *args, **kwargs):
        # Get the manager_id from the URL parameters
        manager_id = kwargs.get('manager_id')

        # Ensure the manager_id is provided
        if not manager_id:
            return Response(
                {"error": "manager_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve all users managed by the specified manager_id
            users = User.objects.filter(manager_id=manager_id)

            # Check if any users were found
            if not users.exists():
                return Response(
                    {"error": "No users found for the given manager_id."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the user data
            serializer = UserSerializer(users, many=True)

            # Return the serialized user data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserDetailView(APIView):

    def get(self, request, user_id, *args, **kwargs):
        try:
            # Fetch the user by ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        # Serialize the user data
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        # Validate and update fields
        data = request.data
        allowed_fields = ["name", "email", "username", "role", "profile_picture", "password"]

        for field, value in data.items():
            if field not in allowed_fields:
                raise ValidationError(f"{field} is not a valid field for updating.")

            if field == "password":
                # Hash the new password before saving
                user.password = make_password(value)
            else:
                setattr(user, field, value)

        user.save()

        # Serialize updated user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePasswordView(APIView):


    def put(self, request, user_id):
        user = User.objects.get(id=user_id)

        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')

        if not old_password or not new_password:
            raise ValidationError({"detail": "Both old and new passwords are required."})

        if not check_password(old_password, user.password):
            raise ValidationError({"detail": "Old password is incorrect."})

        user.password = make_password(new_password)
        user.save()

        return Response({"detail": "Password updated successfully."})

class UploadProfilePictureView(APIView):

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({"detail": "User not found."})

        if 'profile_picture' not in request.FILES:
            raise ValidationError({"detail": "No profile picture uploaded."})

        # Save the uploaded file
        file = request.FILES['profile_picture']
        user.profile_picture.save(file.name, file)
        user.save()

        return Response({"detail": "Profile picture uploaded successfully."})


class DeleteProfilePictureView(APIView):
    """
    API View to delete a user's profile picture.
    """
    def delete(self, request, user_id, *args, **kwargs):
        try:
            # Fetch the user by ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        # Check if the user has a profile picture
        if not user.profile_picture:
            return Response({"detail": "No profile picture to delete."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the file path
        profile_picture_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)

        # Delete the file if it exists
        if os.path.exists(profile_picture_path):
            os.remove(profile_picture_path)

        # Remove the profile picture reference from the user model
        user.profile_picture = None
        user.save()

        return Response({"detail": "Profile picture deleted successfully."}, status=status.HTTP_200_OK)