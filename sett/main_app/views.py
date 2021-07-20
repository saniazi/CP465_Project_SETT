from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (RegisterForm, RegisterFormStudent, RegisterFormSupervisor, 
    TimeSheetEntryForm, UpdatePositionForm, UpdateStudentForm, UpdateSupervisorForm)
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.urls import reverse
from .decorators import *
from django.core.exceptions import PermissionDenied
import datetime

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
        return redirect('admin:index')
    
    raise Http404


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        # Register as student
        if 'student-id_student' in request.POST:
            return register(request, 'student', RegisterForm, RegisterFormStudent)
        # Register as supervisor
        elif 'super-id_supervisor' in request.POST:
            return register(request, 'super', RegisterForm, RegisterFormSupervisor)
        #Login user
        else:
            email = request.POST.get('email')
            password =request.POST.get('pass')
            user = authenticate(request, username=email, password=password)
            
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email or password is incorrect')
                return redirect('login')
    else:
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
    if user_form.is_valid() and custom_form.is_valid():
        # Register user and update required fields
        user = user_form.save()
        custom_user = custom_form.save()

        custom_user.user = user
        user.username = user.email = custom_user.email
        custom_user.save(update_fields=['user'])   
        user.save(update_fields=['username', 'email'])

        # Log in user
        auth_user = authenticate(request, username=custom_user.email, password=request.POST[f'{prefix}-password1'])
        if auth_user:      
            login(request, auth_user)
            return JsonResponse({'status': 0, 'redirect': reverse('home')})
        else:
            messages.error(request, 'Error: Could not log in after registering.')
            return JsonResponse({'status': 0, 'redirect': reverse('login')})

    else:
        errors = {**user_form.errors, **custom_form.errors}
        return JsonResponse({'status': 1, 'errors': errors})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(['student'])
def student_dashboard(request):
    if request.method == 'POST':
        # Add new entry
        if 'add' in request.POST:
            if TimeSheetEntry.objects.all().count() >= 100:
                return JsonResponse({'limit_reached': ''})
            form = TimeSheetEntryForm(request.POST, prefix="add")
        # Update existing entry
        elif 'update' in request.POST:
            pk = request.POST.get('pk')
            entry = TimeSheetEntry.objects.get(pk=pk)
            form = TimeSheetEntryForm(request.POST, prefix="update", instance=entry)
        # Delete entry
        elif 'delete' in request.POST:
            pk = request.POST.get('pk')
            TimeSheetEntry.objects.filter(pk=pk).delete()
            return JsonResponse({})
        else:
            return redirect('student-dash')

        if form.is_valid():
            data = {}
            form.save()
        else:
            data = form.errors.as_json()

        return JsonResponse(data)
        
    entry_form = TimeSheetEntryForm(prefix="add", user=request.user)
    update_form = TimeSheetEntryForm(prefix="update", user=request.user)
    context = {'add_form': entry_form, 'update_form': update_form, 'title': 'Dashboard'}
    
    return render(request, "main_app/student_dashboard.html", context)


@login_required(login_url='login')
@allowed_users(['supervisor'])
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

    context = {'title': 'Dashboard'}
    return render(request, "main_app/supervisor_dashboard.html", context)


# Update timesheet entry status
def update_status(pks, approved, rejected):
    entries = TimeSheetEntry.objects.filter(pk__in=pks)
    for entry in entries:
        entry.approved = approved
        entry.rejected = rejected
        entry.save(update_fields=['approved', 'rejected'])


# Responds to ajax request and gets timesheet entries
def get_entries(request):
    if request.method == 'GET' and 'source' in request.GET:
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
            
            employee = str(entry.job.supervisor) if source == 'student' else str(entry.job.student)
            user_id = entry.job.supervisor.user.id if source == 'student' else entry.job.student.user.id
            # Data to send to datatable through ajax
            data.append(dict(
                date=str(entry.date),
                job=str(entry.job.job_id),
                position=entry.job.position,
                emp_info=f"{employee} {user_id}",
                start_time=entry.start_time.strftime('%I:%M %p'),
                end_time=entry.end_time.strftime('%I:%M %p'),
                hours=str(entry.hours),
                wage='$'+str(entry.job.wage),
                season=entry.job.season,
                status=status,
                id=entry.id
            ))

        return JsonResponse(data, safe=False)
    else:
        raise PermissionDenied


@login_required(login_url='login')
@allowed_users(['supervisor'])
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
        
    # Get jobs associated with current supervisor
    jobs = Job.objects.filter(supervisor=request.user.supervisor)
    context = {'form': form, 'jobs': jobs, 'selected': selected, 'title': 'Positions'}
    return render(request, 'main_app/update_position.html', context)


def get_job(request):
    if request.method == 'GET' and 'job_id' in request.GET:
        job = Job.objects.get(job_id=request.GET['job_id'])
        data = {
            'position': job.position,
            'wage': job.wage,
            'season': job.season,
            'student': str(job.student)
        }
        return JsonResponse(data)
    else:
        raise PermissionDenied


@login_required(login_url='login')
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
            messages.warning(request, 'Update profile disabled on demo.')
            return redirect(reverse(f'profile', args=[pk]))

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