# Generated by Django 3.2.3 on 2021-05-25 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_rename_pay_job_wage'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='overtime',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='hours',
            field=models.IntegerField(default=0),
        ),
    ]
