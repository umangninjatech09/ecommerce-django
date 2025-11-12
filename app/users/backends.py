# users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows login with either email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # If no user with that email, try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        # Check password validity
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
