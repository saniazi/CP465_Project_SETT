from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from . import models

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = models.Student.objects.get(email=username)
            user = student.user
            is_student = True
        except models.Student.DoesNotExist:
            is_student = False
        
        try:
            supervisor = models.Supervisor.objects.get(email=username)
            user = supervisor.user
            is_supervisor = True
        except models.Supervisor.DoesNotExist:
            is_supervisor = False
        
        if is_student or is_supervisor:
            if user.check_password(password):
                return user
            else:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
            else:
                if user.check_password(password):
                    return user
                return None