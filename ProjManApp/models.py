from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.conf import settings


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Member', 'Member'),
        ('Manager', 'Manager'),
    )

    email = models.EmailField(blank=False, max_length=255, unique=True)
    name = models.CharField(blank=False, max_length=255)
    username = models.CharField(blank=False, max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username' 
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name']  

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.username

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)  # Auto-increment ID
    project_name = models.CharField(max_length=255, blank=False)  # Required
    project_description = models.TextField(blank=True, null=True)  # Nullable
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the custom User model
        on_delete=models.CASCADE,  # Delete projects when the user is deleted
        related_name='projects',  # Allows reverse access: user.projects.all()
    )

    def __str__(self):
        return self.project_name
    
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)  # Auto-increment ID
    task_code = models.CharField(max_length=20, unique=True)  # Auto-increment-like task code, e.g. "Task-01"
    features = models.TextField(blank=False)  # Required
    status = models.CharField(max_length=50, blank=True, null=True)  # Nullable field for status
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the custom User model
        on_delete=models.SET_NULL,  # Set to null if user is deleted
        related_name='tasks',  # Allows reverse access: user.tasks.all()
        null=True,  # Nullable
        blank=True,  # Blank allowed for assignee
    )
    sprint = models.IntegerField(blank=True, null=True)  # Integer field for sprint
    priority = models.CharField(max_length=50, blank=False)  # Required
    deadline = models.DateField(blank=False)  # Date field (only date, no time)
    project = models.ForeignKey(
        'Project',  # Reference to the Project model
        on_delete=models.CASCADE,  # Delete tasks when the project is deleted
        related_name='tasks',  # Allows reverse access: project.tasks.all()
    )

    def save(self, *args, **kwargs):
        if not self.task_code:
            last_task = Task.objects.all().order_by('-task_id').first()
            next_task_code = f"Task-{last_task.task_id + 1 if last_task else 1:02d}"
            self.task_code = next_task_code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_code