from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class UsernameOrEmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using either
    their username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Look up the user by username or email
            user = UserModel.objects.get(
                Q(username=username) | Q(email=username)
            )
        except UserModel.DoesNotExist:
            # No user found with the given credentials
            return None

        # Check the password
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        """
        Retrieve a user instance by their ID.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

# Update your settings to use this backend
# Add this to your settings.py:
# AUTHENTICATION_BACKENDS = [
#     'path.to.UsernameOrEmailBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]
