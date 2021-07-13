from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (RegisterForm, RegisterFormStudent, RegisterFormSupervisor, 
    createHoursFormAssistants, YEAR_CHOICES, UpdatePositionForm, UpdateStudentForm,
    UpdateSupervisorForm)
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .decorators import unauthenticated_user
import datetime
import json

# Create your views here.

@login_required(login_url='login')
def home(request):
    # print(request.user.supervisor)
    # print(request.user)
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
        return redirect('student-dash')
    
    if not is_student and is_supervisor:
        return redirect('super-dash')
    
    if request.user.is_superuser:
        #return HttpResponseRedirect(reverse('admin:index'))
        return redirect('admin:index')
    
    raise Http404

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        #print(request.POST)
        if 'student-id_student' in request.POST:
            return register(request, 'student', RegisterForm, RegisterFormStudent)
        elif 'super-id_supervisor' in request.POST:
            return register(request, 'super', RegisterForm, RegisterFormSupervisor)
        else:
            email = request.POST.get('email')
            password =request.POST.get('pass')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email or password is incorrect')
                return redirect('login')
    
    user_form_student = RegisterForm(prefix='student')
    custom_form_student = RegisterFormStudent(prefix='student')

    supervisor_form = RegisterForm(prefix='super')
    custom_supervisor_form = RegisterFormSupervisor(prefix='super')

    context = {
        'student_form': user_form_student, 
        'custom_student_form': custom_form_student,
        'super_form': supervisor_form,
        'custom_super_form': custom_supervisor_form
    }
    
    return render(request, 'main_app/login.html', context)


def register(request, prefix, user_registor_form, custom_registor_form):
    # Supervisor.objects.filter(id_supervisor=15).delete()
    # User.objects.filter(id=39).delete()
    user_form = user_registor_form(request.POST, prefix=prefix)
    custom_form = custom_registor_form(request.POST, prefix=prefix)
    print(user_form.is_valid())
    print(custom_form.is_valid())
    if user_form.is_valid() and custom_form.is_valid():
        user = user_form.save()
        custom_user = custom_form.save()

        custom_user.user = user
        user.username = user.email = custom_user.email
        custom_user.save(update_fields=['user'])   
        user.save(update_fields=['username', 'email'])

        auth_user = authenticate(request, username=custom_user.email, password=request.POST[f'{prefix}-password1'])
        if auth_user:      
            login(request, auth_user)
            print('done')
            return JsonResponse({'status': 0, 'redirect': reverse('home')})
    else:
        errors = {**user_form.errors, **custom_form.errors}
        #print(custom_form.errors.as_json())
        return JsonResponse({'status': 1, 'errors': errors})


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


# @login_required(login_url='login') 
# def profile(request):
#     if request.method == 'POST':
#         #print("Received POST from Profile page")
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         number = request.POST['number']
#         dob = request.POST['dob']
#         dob = datetime.datetime.strptime(dob, '%Y-%m-%d')
#         dob = dob.date()
#         SIN = request.POST['SIN']
#         school_year = int(request.POST['school_year'])

#         # Testing
#         print(f'{type(dob)}')
#         print(first_name, last_name, email, dob, number, SIN)
    

#         db_instance = Student(
#             first_name=first_name,
#             last_name=last_name,
#             dob=dob,
#             email=email,
#             phone=number,
#             school_year=school_year
#             )
#         db_instance.save()
#         print("Form data saved to db")
#         return render(request, "main_app/dashboard_student.html", {'title': 'Dashboard Student'})

#     return render(request, "main_app/profile.html", {'title': 'Profile'})


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


def base(request):
    return render(request, 'main_app/base.html', {})


@login_required(login_url='login')
def student_dashboard(request):
    if request.method == 'POST':
        if 'add' in request.POST:
            form = createHoursFormAssistants(request.POST, prefix="add")
        elif 'update' in request.POST:
            pk = request.POST.get('pk')
            entry = TimeSheetEntry.objects.get(pk=pk)
            form = createHoursFormAssistants(request.POST, prefix="update", instance=entry)
        elif 'delete' in request.POST:
            pk = request.POST.get('pk')
            num_deleted = TimeSheetEntry.objects.filter(pk=pk).delete()

            return HttpResponse(json.dumps({}), content_type='application/json')
        else:
            json_data = json.dumps({'no_action': 'Error: action to perform on form not found.'})

            return HttpResponse(json_data, content_type='application/json')

        if form.is_valid():
            json_data = json.dumps({})
            form.save()
        else:
            json_data = form.errors.as_json()

        return HttpResponse(json_data, content_type='application/json')
        
    entry_form = createHoursFormAssistants(prefix="add", user=request.user)
    update_form = createHoursFormAssistants(prefix="update", user=request.user)
    context = {'add_form': entry_form, 'update_form': update_form}
    
    return render(request, "main_app/student_dashboard.html", context)


@login_required(login_url='login')
def supervisor_dashboard(request):
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST.get('action')
            if action == 'approve':
                update_status(request.POST.getlist('entry_pks'), True, False)
            elif action == 'reject':
                update_status(request.POST.getlist('entry_pks'), False, True)
            else:
                update_status(request.POST.getlist('entry_pks'), False, False)
            return JsonResponse({})

    context = {}
    return render(request, "main_app/supervisor_dashboard.html", context)


def update_status(pks, approved, rejected):
    entries = TimeSheetEntry.objects.filter(pk__in=pks)
    for entry in entries:
        entry.approved = approved
        entry.rejected = rejected
        entry.save(update_fields=['approved', 'rejected'])


def get_entries(request):
    start_date = datetime.datetime.strptime(request.GET.get('start_date'), '%a %b %d %Y')
    end_date = datetime.datetime.strptime(request.GET.get('end_date'), '%a %b %d %Y')
    source = request.GET.get('source')
    if source == 'student':
        entries = TimeSheetEntry.objects.filter(job__student=request.user.student, date__range=(start_date, end_date))
    else:
        entries = TimeSheetEntry.objects.filter(job__supervisor=request.user.supervisor, date__range=(start_date, end_date))

    data = []
    for entry in entries:
        if entry.approved:
            status = 'Approved'
        elif entry.rejected:
            status = 'Rejected'
        else:
            status = 'Pending approval'
        
        name = str(entry.job.supervisor) if source == 'student' else str(entry.job.student)
        data.append(dict(
            date=str(entry.date),
            job=str(entry.job.job_id),
            position=entry.job.position,
            name=name,
            start_time=entry.start_time.strftime('%I:%M %p'),
            end_time=entry.end_time.strftime('%I:%M %p'),
            hours=str(entry.hours),
            wage='$'+str(entry.job.wage),
            season=entry.job.season,
            status=status,
            id=entry.id
        ))

    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def update_position(request):
    selected = ''
    if request.method == 'POST':
        if 'new' in request.POST:
            form = UpdatePositionForm(request.POST)
            if form.is_valid():
                job = form.save()
                messages.success(request, f'Successfully added job {job.job_id}!')
                return redirect('positions')
            else:
                messages.warning(request, 'Please correct the errors below.')
        elif 'save' in request.POST:
            selected = request.POST['job_id']
            job = Job.objects.get(job_id=selected)
            form = UpdatePositionForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, f'Successfully saved job {selected}!')
                return redirect('positions')
            else:
                messages.warning(request, 'Please correct the errors below.')
        elif 'delete' in request.POST:
            selected = request.POST['job_id']
            job = Job.objects.get(job_id=selected).delete()
            messages.success(request, f'Successfully deleted job {selected}!')
            return redirect('positions')
    else:
        form = UpdatePositionForm(user=request.user, 
            initial={'supervisor': request.user.supervisor})
        
    jobs = Job.objects.filter(supervisor=request.user.supervisor)
    context = {'form': form, 'jobs': jobs, 'selected': selected}
    return render(request, 'main_app/update_position.html', context)


def get_job(request):
    job = Job.objects.get(job_id=request.GET['job_id'])
    data = {
        'position': job.position,
        'wage': job.wage,
        'season': job.season,
        'student': str(job.student)
    }
    return JsonResponse(data)


def profile(request, pk):
    user = User.objects.filter(pk=pk)
    if user:
        if hasattr(user[0], 'student'):
            user_group = user[0].student
            modelform = UpdateStudentForm
        elif hasattr(user[0], 'supervisor'):
            user_group = user[0].supervisor
            modelform = UpdateSupervisorForm
        else:
            raise Http404

        if request.method == 'POST' and request.user.id == pk:
            form = modelform(request.POST, request.FILES, instance=user_group)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your profile has been updated!')
                return redirect(reverse(f'profile', args=[pk]))
            else:
                messages.warning(request, 'Please correct the errors below.')
        else:
            form = modelform(instance=user_group)

        context = {'user': user_group, 'pk': pk, 'form': form}
        return render(request, 'main_app/profile.html', context)
    else:
        raise Http404