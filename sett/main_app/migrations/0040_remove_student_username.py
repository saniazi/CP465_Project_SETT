# Generated by Django 3.2.3 on 2021-06-28 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0039_alter_student_first_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='username',
        ),
    ]