from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, RegisterFormStudent, RegisterFormSupervisor, createHoursFormAssistants
from .forms import RegisterForm, RegisterFormStudent, RegisterFormSupervisor, YEAR_CHOICES
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .decorators import unauthenticated_user
import datetime

# Create your views here.

@login_required(login_url='login')
def home(request):
    try:
        Student.objects.get(user=request.user)
        is_student = True
    except Student.DoesNotExist:
        is_student = False

    try:
        Supervisor.objects.get(user=request.user)
        is_supervisor = True
    except Supervisor.DoesNotExist:
        is_supervisor = False

    if is_student and not is_supervisor:
        return redirect('dashboard-student')
    
    if not is_student and is_supervisor:
        return redirect('dashboard-supervisor')
    
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))
    
    raise Http404

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password =request.POST.get('pass')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password is incorrect')
            return redirect('login')
    
    return render(request, 'main_app/login2.html')


def logout_view(request):
    logout(request)
    return redirect('login')


#@login_required(login_url='login')
def dashboard_supervisor(request):
    if request.method == 'POST':
        jobs = Job.objects.all().filter(supervisor=request.user.supervisor, approved=False)
        job_ids = request.POST.getlist('approved')
        for job_id in job_ids:
            try:
                job = Job.objects.get(id_job=job_id)
            except Job.DoesNotExist:
                return redirect('dashboard-supervisor')
            else:
                job.approved = True
                job.save()

    jobs = Job.objects.all().filter(supervisor=request.user.supervisor, approved=False)
    context = {'jobs': jobs}
    return render(request, "main_app/dashboard_supervisor.html", context)


@login_required(login_url='login')
def dashboard_student(request):
    jobs = Job.objects.all().filter(student=request.user.student)
    total_hours = 0
    amount = 0
    for job in jobs:
        total_hours += job.hours
        amount += job.hours * job.pay

    context = {'jobs': jobs, 'total_hours': total_hours, 'amount': amount}
    return render(request, "main_app/dashboard_student.html", context)


#@login_required(login_url='login')
def hoursFormAssistants(request):
    form = createHoursFormAssistants(request.POST)
    if form.is_valid():
        print("valid")
    return render(request, 'main_app/hoursFormAssistants.html', {'form':form})

    # old used with html
    # if request.method == 'POST':
    #     hours_date = request.POST['hours_date']
    #     hours_date = datetime.datetime.strptime(hours_date, '%Y-%m-%d')
    #     hours_date = hours_date.date()

    #     start_time = request.POST['start_time']
    #     end_time = request.POST['end_time']

    #     supervisor_name = request.POST['supervisor_name']

    #     # To do
    #     # Get year radio buttons values
    #    # year_2 = request.POST['year_2']
    #     #year_3 = request.POST['year_3']
        
    #     form = YEAR_CHOICES(request.POST)
    #     selected = form.cleaned_data.get("YEAR")
    #     print(selected)

    #     # To do
    #     # Get hazard pay radio button value

    #     # Testing
    #     print("Received POST from hoursFormAssistants page")
    #     print(supervisor_name)
    #     print(hours_date)
    #     print(start_time)
    #     print(end_time)
    #     #print(year_2)
    #     #print(year_3)

    #     return render(request, "main_app/dashboard_student.html", {'title': 'Dashboard Student'})
        

    # return render(request, "main_app/hoursFormAssistants.html", {'title': 'Assistant Form'})


@login_required(login_url='login')
def hoursFormRegular(request):
    if request.method == 'POST':
        hours_date = request.POST['hours_date']
        hours_date = datetime.datetime.strptime(hours_date, '%Y-%m-%d')
        hours_date = hours_date.date()

        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        start_time = datetime.datetime.strptime(start_time, '%H:%M')  
        end_time = datetime.datetime.strptime(end_time, '%H:%M')
        hours = (end_time-start_time)
        hours = hours.days * 24 + hours.seconds/3600

        job_id = request.POST['job_id']

        # Testing
        print("Received POST from hoursFormRegular page")
        print(hours_date)
        print(start_time)
        print(end_time)
        print(end_time-start_time)

        try:
            job = Job.objects.get(student=request.user.student, id_job=job_id)
        except Job.DoesNotExist:
            messages.error(request, "Job ID is not assigned to current user. Please try again")
            return redirect('hours-form-regular')
        else:
            job.dateHours = hours_date
            job.startTime = start_time
            job.endTime = end_time
            job.hours = hours
            job.save()
            messages.success(request, 'Hours successfully submitted')

    return render(request, "main_app/hoursFormRegular.html")


@login_required(login_url='login') 
def profile(request):
    if request.method == 'POST':
        #print("Received POST from Profile page")
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        number = request.POST['number']
        dob = request.POST['dob']
        dob = datetime.datetime.strptime(dob, '%Y-%m-%d')
        dob = dob.date()
        SIN = request.POST['SIN']
        school_year = int(request.POST['school_year'])

        # Testing
        print(f'{type(dob)}')
        print(first_name, last_name, email, dob, number, SIN)
    

        db_instance = Student(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            sin=SIN,
            email=email,
            phone=number,
            school_year=school_year
            )
        db_instance.save()
        print("Form data saved to db")
        return render(request, "main_app/dashboard_student.html", {'title': 'Dashboard Student'})

    return render(request, "main_app/profile.html", {'title': 'Profile'})


@unauthenticated_user
def student_register(request):
    if request.method == 'POST':
        form_user = RegisterForm(request.POST)
        form_custom_user = RegisterFormStudent(request.POST)
        if form_user.is_valid() and form_custom_user.is_valid():
            user = form_user.save()
            Student.objects.create(user=user, username=user.username)
            form_custom_user = RegisterFormStudent(request.POST, instance=user.student)
            form_custom_user.full_clean()
            form_custom_user.save()
            messages.success(request, f'Registration successful! You may now login.')
            return redirect('login')
    else:
        form_user = RegisterForm()
        form_custom_user = RegisterFormStudent()
    context = {'form_user': form_user, 'form_custom_user': form_custom_user}
    return render(request, 'main_app/student_register.html', context)


@unauthenticated_user
def supervisor_register(request):
    if request.method == 'POST':
        form_user = RegisterForm(request.POST)
        form_custom_user = RegisterFormSupervisor(request.POST)
        if form_user.is_valid() and form_custom_user.is_valid():
            user = form_user.save()
            Supervisor.objects.create(user=user, username=user.username)
            form_custom_user = RegisterFormSupervisor(request.POST, instance=user.supervisor)
            form_custom_user.full_clean()
            form_custom_user.save()
            messages.success(request, f'Registration successful! You may now login.')
            return redirect('login')
    else:
        form_user = RegisterForm()
        form_custom_user = RegisterFormSupervisor()
    context = {'form_user': form_user, 'form_custom_user': form_custom_user}
    return render(request, 'main_app/supervisor_register.html', context)
 