from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from . import models

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        student = models.Student.objects.filter(email=username)
        supervisor = models.Supervisor.objects.filter(email=username)
        user = User.objects.filter(username=username)
        if student or supervisor:
            user = student[0].user if student else supervisor[0].user
            if user.check_password(password):
                return user
        elif user and user[0].check_password(password):
            return user[0]
            
        return None