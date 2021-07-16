from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
import datetime

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/images/profile_pics/<user.id>/<filename>
        return f'images/profile_pics/{instance.user.id}/{filename}'


class Department(models.Model):
    dep_name = models.CharField(max_length=200)

    def __str__(self):
	    return self.dep_name

    class Meta:
        #managed = False
        db_table = 'department'


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

    job_id = models.AutoField(primary_key=True, validators=[MinValueValidator(0), MaxValueValidator(99999999)])
    wage = models.DecimalField(max_digits=6, decimal_places=2)
    season = models.CharField(max_length=6, choices=SEASON_CHOICES)
    student = models.ForeignKey('Student', models.CASCADE)
    supervisor = models.ForeignKey('Supervisor', models.CASCADE)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES) 
   
    def __str__(self):
	    return str(self.job_id)

    class Meta:
        #managed = False
        db_table = 'job'


class TimeSheetEntry(models.Model):
    date = models.DateField(default=datetime.date.today)
    job = models.ForeignKey('Job', models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

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
    SCHOOL_YEARS = [1, 2, 3, 4, 5, 6]
    YEAR_CHOICES = [
        (SCHOOL_YEARS[0], '1'),
        (SCHOOL_YEARS[1], '2'),
        (SCHOOL_YEARS[2], '3'),
        (SCHOOL_YEARS[3], '4'),
        (SCHOOL_YEARS[4], '5'),
        (SCHOOL_YEARS[5], '6')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    id_student = models.IntegerField(
        primary_key=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        error_messages={
            'unique': 'Student with this ID is already registered.'
        }
    )
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'This email is already registered.'
        }
    )
    phone = models.CharField(max_length=18, blank=True)
    school_year = models.IntegerField(choices=YEAR_CHOICES)
    profile_pic = models.ImageField(default="images/profile_pics/default.png", upload_to=user_directory_path)

    def __str__(self):
	    return str(self.id_student)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    class Meta:
        #managed = False
        db_table = 'student'


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    id_supervisor = models.IntegerField(primary_key=True, error_messages={
        'unique': 'Supervisor with this ID is already registered.'
        })
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'This email is already registered.'
        }
    )
    phone = models.CharField(max_length=18, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    profile_pic = models.ImageField(default="images/profile_pics/default.png", upload_to=user_directory_path)

    def __str__(self):
	    return str(self.id_supervisor)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    class Meta:
        #managed = False
        db_table = 'supervisor'
