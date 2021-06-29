from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from .models import Student, Supervisor, Job, TimeSheetEntry


def custom_validity(field_name):
    return {
            'oninvalid': f'this.setCustomValidity("{field_name} is required.")',
            'oninput': 'this.setCustomValidity("")'
    }

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'oninvalid': 'this.setCustomValidity("Please enter a password.")',
            'oninput': 'this.setCustomValidity("")'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'oninvalid': 'this.setCustomValidity("Please confirm password.")',
            'oninput': 'this.setCustomValidity("")'
        })

    class Meta:
        model = User
        fields = ['password1', 'password2']


class LoginFormView(SuccessMessageMixin, auth_views.LoginView):
    success_message = "Login Successful"


class RegisterFormStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id_student', 'first_name', 'last_name', 'dob', 'school_year', 'phone', 'email']
        labels = {
            'id_student': 'Student ID',
            'dob': 'Date of birth',
            'phone': 'Phone number'
        }
        widgets = {
            'id_student': forms.NumberInput(attrs=custom_validity('Student ID')),
            'first_name': forms.TextInput(attrs=custom_validity('First name')),
            'last_name': forms.TextInput(attrs=custom_validity('Last name')),
            'dob': forms.DateInput(attrs={**custom_validity('Date of birth'), **{'type': 'date'}}),
            'school_year': forms.Select(attrs=custom_validity('School year')),
            'phone': forms.TextInput(attrs={'placeholder': 'e.g. 123-456-7890'}),
            'email': forms.TextInput(attrs=custom_validity('Email'))
        }


class RegisterFormSupervisor(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['id_supervisor', 'first_name', 'last_name', 'department', 'phone', 'email']
        labels = {
            'id_supervisor': 'ID',
            'phone': 'Phone number'
        }
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'e.g. 123-456-7890'}),
            'id_supervisor': forms.NumberInput(attrs=custom_validity('Supervisor ID')),
            'first_name': forms.TextInput(attrs=custom_validity('First name')),
            'last_name': forms.TextInput(attrs=custom_validity('Last name')),
            'department': forms.TextInput(attrs=custom_validity('Department name')),
            'email': forms.TextInput(attrs=custom_validity('Email'))
        }


YEAR = [
    ('one', 'one'),
    ('two', 'two'),
]


class YEAR_CHOICES(forms.Form):
    YEAR = forms.CharField(widget=forms.RadioSelect(choices=YEAR))


class createHoursFormAssistants(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(createHoursFormAssistants, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['job'].queryset = Job.objects.filter(student=user.student)

    class Meta:
        model = TimeSheetEntry
        fields = [
            'job',
            'date',
            'start_time',
            'end_time'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            'job': 'Job ID',
            'date': 'Date',
            'start_time': 'Time In',
            'end_time': 'Time Out'
        }

