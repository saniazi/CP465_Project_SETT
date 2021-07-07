"""sett URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views as main_views
from django.contrib.auth import views as auth_views
from .forms import LoginFormView
from django.conf.urls import include, url


urlpatterns = [
    path('', main_views.home, name='home'),
    path('login/', main_views.login_view, name='login'),
    path('logout/', main_views.logout_view, name='logout'),
    path('dashboard_supervisor/', main_views.dashboard_supervisor, name='dashboard-supervisor'),
    path('student_register/', main_views.student_register, name='register-student'),
    path('supervisor_register/', main_views.supervisor_register, name='register-supervisor'),
    path('dashboard_student/', main_views.dashboard_student, name='dashboard-student'),
    path('profile/hoursFormAssistants/', main_views.hoursFormAssistants, name='hours-form-assistants'),
    path('profile/hoursFormRegular/', main_views.hoursFormRegular, name='hours-form-regular'),
    path('profile/', main_views.profile, name='profile'),
    path('base/', main_views.base, name='base'),
    path('student_dashboard/', main_views.student_dashboard, name='student-dash'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('supervisor_dashboard/', main_views.supervisor_dashboard, name='super-dash'),
    path('get_entries/', main_views.get_entries, name='get_entries'),
    path('update_position/', main_views.update_position, name='positions'),
    path('get_job/', main_views.get_job, name='get_job'),
]
