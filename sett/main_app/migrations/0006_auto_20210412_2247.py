# Generated by Django 3.1.7 on 2021-04-12 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20210412_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='dateHours',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='endTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='hazardous',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='startTime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='studentYear',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
