from django.contrib import admin
from .models import Job, Student, Supervisor, Department
#from .models import Student

# Register your models here.
admin.site.register(Job)
admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Department)