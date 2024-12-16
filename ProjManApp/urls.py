from django.urls import path
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/register', views.register, name='register'),
    path('api/projects/create', ProjectCreateView.as_view(), name='create_project'),
    path('projects/<int:manager_id>/', ProjectCreateView.as_view(), name='project-by-user'),
    path('tasks/<int:project_id>/', TaskListView.as_view(), name='task-list'),  # GET: List tasks by project_id
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),  # POST: Create a task
    path('tasks/edit/<int:task_id>/', TaskEditView.as_view(), name='task-edit'),
    path('tasks/assign/<int:task_id>/', TaskAssignEditView.as_view(), name='task-edit'),
    path('manager/<int:manager_id>/', UserListView.as_view(), name='user-list-by-manager'),
    path('manager/create/', UserCreateView.as_view(), name='user-create'),
    path('manager/edit/<int:pk>/', UserUpdateView.as_view(), name='user-edit'),
    path('user/<int:pk>/deactivate/', UserIsActiveUpdateView.as_view(), name='user-deactivate'),
    path('api/projects/update/<int:project_id>/', ProjectCreateView.as_view(), name='update_project'),
    path('api/projects/archive/<int:project_id>/', ArchiveProjectView.as_view(), name='archive_project'),
    path('projects/archives/<int:manager_id>/', ArchiveProjectView.as_view(), name='archived-projects'),
    path('api/projects/unarchive/<int:project_id>/', UnarchiveProjectView.as_view(), name='archive_project'),
    # This handles listing and creating reports
    path('reports/create_report/', ReportListCreateAPIView.as_view(), name='report-list-create'),
    path('files/create/', FileCreateAPIView.as_view(), name='file-create'),
    path('files/project/<int:project_id>/', FileListByProjectAPIView.as_view(), name='file-list-by-project'),
    # This handles updating a specific report by its ID
    path('reports/<int:report_id>/', ReportUpdateAPIView.as_view(), name='report-update'),
    path('api/tasks/filter/', FilterTasksAPIView.as_view(), name='filter_tasks'),
    path('api/tasks/completion-percentage/', TaskCompletionPercentageAPIView.as_view(),
         name='task-completion-percentage'),
    path('users/manager/<int:manager_id>/', UserByManagerAPIView.as_view(), name='users-by-manager'),
    path('api/userprofile/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/updatepass/<int:user_id>/', UpdatePasswordView.as_view(), name='update-pass'),
    path('api/uploadpicture/<int:user_id>/', UploadProfilePictureView.as_view(),
         name='upload-profile-picture'),

    path('api/deletepicture/<int:user_id>/', DeleteProfilePictureView.as_view(),
         name='delete-profile-picture'),
    path('user/<int:user_id>/delete/', DeleteUserView.as_view(), name='delete-user'),
    path('api/add-log/', AddLogAPIView.as_view(), name='add-log'),
    path('api/logs/<int:project>/', LogAPIView.as_view(), name='add-log'),
    path('api/notifications/', NotificationListCreate.as_view(), name='notification-list-create'),
    path('api/notifications/<int:notification_id>/', NotificationListCreate.as_view(), name='notification-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

