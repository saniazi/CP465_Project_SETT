# Generated by Django 3.2.3 on 2021-06-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_auto_20210617_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='school_year',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]
