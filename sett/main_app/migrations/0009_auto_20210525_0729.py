# Generated by Django 3.2.3 on 2021-05-25 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_job_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.student'),
        ),
        migrations.AlterField(
            model_name='job',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.supervisor'),
        ),
    ]
