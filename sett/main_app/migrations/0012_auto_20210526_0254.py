# Generated by Django 3.2.3 on 2021-05-26 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_auto_20210525_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='id_job',
            field=models.PositiveIntegerField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='overtime',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='position',
            field=models.CharField(choices=[('TA', 'Teaching Assistant'), ('Lab Assistant', 'Lab Assistant'), ('Marker', 'Marker'), ('Proctor', 'Proctor')], default='TA', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='season',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Winter', 'Winter'), ('Spring', 'Spring')], default='Fall', max_length=6),
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateHours', models.DateField(blank=True, null=True)),
                ('startTime', models.DateField(blank=True, null=True)),
                ('endTime', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('id_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.job')),
            ],
            options={
                'db_table': 'time_sheet',
            },
        ),
    ]
