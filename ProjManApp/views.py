from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from .forms import CreateUserForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Report, Log, Notification
from .serializers import ProjectSerializer, ReportSerializer, LogSerializer, NotificationSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
import os
from django.conf import settings
from rest_framework.viewsets import ReadOnlyModelViewSet



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
    # Parse the incoming data and form from the request
    data = json.loads(request.body.decode('utf-8'))

    # Ensure to handle the files in request.FILES (for profile picture upload)
    form = CreateUserForm(data, request.FILES)

    if form.is_valid():
        # Save the user form
        user = form.save()

        # Check if the profile picture is provided
        if 'profile_picture' in request.FILES:
            file = request.FILES['profile_picture']
            # Save the uploaded file as profile picture for the user
            user.profile_picture.save(file.name, file)

        user.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        # Return errors if the form is not valid
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

        # Get the cancelled filter from query parameters, default to False
        cancelled = self.request.query_params.get('excludeCancelled', 'false').lower() == 'true'

        # Filter tasks by project_id
        queryset = Task.objects.filter(project_id=project_id)

        # Optionally filter by status
        if status:
            queryset = queryset.filter(status=status)

        # Filter out cancelled tasks if cancelled=false
        if cancelled:
            queryset = queryset.exclude(status="Cancelled")

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
    and status = 'In Progress' OR 'Not Started' OR 'Completed'.
    """
    def get(self, request, *args, **kwargs):
        project_id = self.request.query_params.get('project_id')
        assignee_id = self.request.query_params.get('assignee_id')
        status_param = self.request.query_params.get('status')  # Get the status filter if provided

        # Ensure parameters are provided
        if not project_id or not assignee_id:
            return Response(
                {"error": "Project ID and Assignee ID are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Build the filter for the task status
        status_filter = Q(status="In Progress") | Q(status="Not started")
        if status_param and status_param.lower() == "completed":
            status_filter |= Q(status="Completed")

        try:
            tasks = Task.objects.filter(
                project_id=project_id,
                assignee_id=assignee_id
            ).filter(status_filter)  # Apply the dynamic status filter

            # Serialize the tasks
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

class DeleteUserView(APIView):
    """
    API View to delete a user based on user_id.
    Only authorized personnel (e.g., admins) can perform this action.
    """

    def delete(self, request, user_id, *args, **kwargs):
        try:
            # Fetch the user by ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")

        # Delete the user
        user.delete()

        return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)

class AddLogAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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


class LogAPIView(APIView):
    """
    APIView for listing logs and applying filters.
    """

    def get(self, request, project=None,*args, **kwargs):
        # Get query parameters
        user_created = request.query_params.get('log_user_created')

        # Base queryset
        queryset = Log.objects.all().order_by('-log_datetime')

        # Apply filters
        if user_created:
            queryset = queryset.filter(log_user_created=user_created)

        queryset = queryset.filter(log_project=project)

        # Serialize data
        serializer = LogSerializer(queryset, many=True)

        # Return response
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationListCreate(APIView):

    # GET method to retrieve all notifications with optional filter by user concerned
    def get(self, request):
        # Get the user to filter by from query params
        user_concerned = request.query_params.get('user', None)
        project_id = request.query_params.get('project_id', None)

        if user_concerned:
            # Filter notifications by the concerned user (notification_user_concern)
            notifications = Notification.objects.filter(notification_user_concern=user_concerned)
        else:
            # Retrieve all notifications if no filter is provided
            notifications = Notification.objects.all().order_by('-notification_datetime')

        if project_id:
            notifications = notifications.filter(notification_project=project_id)

        notifications = notifications.order_by('-notification_datetime')



        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    # POST method to create a new notification
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Optionally associate with logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, notification_id=None):
        try:
            # Fetch the notification by its ID
            notification = Notification.objects.get(notification_id=notification_id)
            notification.delete()  # Delete the notification
            return Response({"message": "Notification deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            # Return an error if the notification does not exist
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)