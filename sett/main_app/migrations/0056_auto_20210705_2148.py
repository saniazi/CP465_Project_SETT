# Generated by Django 3.2.3 on 2021-07-05 21:48

from django.db import migrations


def default_departments(apps, schema_editor):
    departments = ['Biology', 'Business', 'Communication Studies', 'Economics', 'History', 'Mathematics', 'Philosophy', 'Physics and Computer Science']
    Department = apps.get_model('main_app', 'Department')

    for department in departments:
        Department.objects.create(dep_name=department)


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0055_auto_20210705_0654'),
    ]

    operations = [
        migrations.RunPython(default_departments),
    ]
