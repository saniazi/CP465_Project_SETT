# Generated by Django 3.2.3 on 2021-07-06 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0059_alter_supervisor_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=18),
        ),
    ]
