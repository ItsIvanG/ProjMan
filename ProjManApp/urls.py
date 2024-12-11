from django.urls import path
from . import views
from .views import ProjectCreateView
from .views import TaskCreateView, TaskListView


urlpatterns = [
    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/register', views.register, name='register'),
    path('api/projects/create', ProjectCreateView.as_view(), name='create_project'),
    path('projects/<int:user_id>/', ProjectCreateView.as_view(), name='project-by-user'), 
    path('tasks/<int:project_id>/', TaskListView.as_view(), name='task-list'),  # GET: List tasks by project_id
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),  # POST: Create a task
]
