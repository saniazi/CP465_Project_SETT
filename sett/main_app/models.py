from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Department(models.Model):
    id_department = models.AutoField(primary_key=True)
    job = models.ForeignKey('Job', models.DO_NOTHING, blank=True, null=True)
    dep_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Job(models.Model):
    TEACHING_ASSISTANT = 'TA'
    LAB_ASSISTANT = 'Lab Assistant'
    MARKER = 'Marker'
    PROCTOR = 'Proctor'
    FALL = 'Fall'
    WINTER = 'Winter'
    SPRING = 'Spring'

    POSITION_CHOICES = [
        (TEACHING_ASSISTANT, 'Teaching Assistant'),
        (LAB_ASSISTANT, 'Lab Assistant'),
        (MARKER, 'Marker'),
        (PROCTOR, 'Proctor')
    ]
    SEASON_CHOICES = [
        (FALL, 'Fall'),
        (WINTER, 'Winter'),
        (SPRING, 'Spring')
    ]

    job_id = models.IntegerField(primary_key=True, validators=[MinValueValidator(0), MaxValueValidator(99999999)])
    wage = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    season = models.CharField(max_length=6, choices=SEASON_CHOICES, default=FALL)
    student = models.ForeignKey('Student', models.CASCADE, blank=True, null=True)
    supervisor = models.ForeignKey('Supervisor', models.CASCADE, blank=True, null=True)
    approved = models.BooleanField(default=False)
    position = models.CharField(max_length=100, null=True, choices=POSITION_CHOICES, default=TEACHING_ASSISTANT)
    
    dateHours = models.DateField(blank=True, null=True)
    startTime = models.DateField(blank=True, null=True)
    endTime = models.DateField(blank=True, null=True)

    # to do
    # Caculate hours from startTime and endTime
    hours = models.PositiveIntegerField(default=0)
    overtime = models.PositiveIntegerField(default=0)

    # hazardous = models.CharField(max_length=3, blank=True, null=True)
    # studentYear = models.IntegerField(blank=True, null=True)
    #studentYear = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True)
    def __str__(self):
	    return f"{self.job_id}"

    class Meta:
        #managed = False
        db_table = 'job'


class TimeSheetEntry(models.Model):
    date = models.DateField(default=datetime.date.today)
    job = models.ForeignKey('Job', models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    approved = models.BooleanField(default=False)

    @property
    def hours(self):
        if self.start_time > self.end_time:
            end_date_time = datetime.datetime.combine(datetime.date.min + datetime.timedelta(days=1), self.end_time)
        else:
            end_date_time = datetime.datetime.combine(datetime.date.min, self.end_time)
        
        start_date_time = datetime.datetime.combine(datetime.date.min, self.start_time)
        diff = end_date_time - start_date_time
        diff = diff.total_seconds()
        diff = round((diff/3600)*4)/4
        return diff

    def __str__(self):
	    return f"Date: {self.date} Job: {self.job.job_id}"
    
    class Meta:
        db_table = 'time_sheet_entry'
        constraints = [models.UniqueConstraint(fields=['date', 'job', 'start_time', 'end_time'], name='unique_entry')]


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_student = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    school_year = models.IntegerField(blank=True, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)

    def __str__(self):
	    return f"{self.first_name} {self.last_name}"

    class Meta:
        #managed = False
        db_table = 'student'


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    id_supervisor = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    sin = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)

    def __str__(self):
	    return f"{self.first_name} {self.last_name}"

    class Meta:
        #managed = False
        db_table = 'supervisor'

# class StudentHours(models.Model):
#     hoursDate = models.DateField(blank=True, null=True)
#     startTime = models.DateField(blank=True, null=True)
#     endTime = models.DateField(blank=True, null=True)
#     supervisor = models.CharField(max_length=200, blank=True, null=True)
#     studentYear = models.IntegerField(blank=True, null=True)
#     hazardous = models.CharField(max_length=3, blank=True, null=True)
    
#     # Connect to other tables
#     # student = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True)
    
#     def __str__(self):
# 	    return f"{self.first_name} {self.last_name}"

#     class Meta:
#         #managed = False
#         db_table = 'studentHours'
