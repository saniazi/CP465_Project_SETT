# Generated by Django 3.2.3 on 2021-06-26 09:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0028_alter_student_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='id_student',
            field=models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999999999)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]