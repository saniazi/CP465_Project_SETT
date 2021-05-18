from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from .models import Student, Supervisor, Job


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginFormView(SuccessMessageMixin, auth_views.LoginView):
    success_message = "Login Successful"

class RegisterFormStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['sin', 'id_student', 'dob', 'school_year', 'phone', 'first_name', 'last_name', 'email']

class RegisterFormSupervisor(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['sin', 'id_supervisor', 'dob', 'department', 'phone', 'first_name', 'last_name', 'email']

YEAR = [
    ('one', 'one'),
    ('two', 'two'),
]
class YEAR_CHOICES(forms.Form):
    YEAR = forms.CharField(widget=forms.RadioSelect(choices=YEAR))

class createHoursFormAssistants(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'dateHours',
            'startTime',
            'endTime',
            'supervisor',
            'hazardous',
        ]

