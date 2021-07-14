# Generated by Django 3.2.3 on 2021-07-05 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0054_alter_job_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='id_department',
        ),
        migrations.RemoveField(
            model_name='department',
            name='job',
        ),
        migrations.AddField(
            model_name='department',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='dep_name',
            field=models.CharField(max_length=200),
        ),
    ]