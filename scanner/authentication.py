# authentication.py (create this file inside your app)

from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                print(f"Password mismatch for email: {email}")
        except CustomUser.DoesNotExist:
            print(f"User with email {email} does not exist.")
        return None

