# Generated by Django 3.2.3 on 2021-07-06 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0058_rename_dept_supervisor_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.department'),
        ),
    ]
