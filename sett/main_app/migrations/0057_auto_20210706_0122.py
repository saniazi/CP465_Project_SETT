# Generated by Django 3.2.3 on 2021-07-06 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0056_auto_20210705_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisor',
            name='department',
        ),
        migrations.AddField(
            model_name='supervisor',
            name='dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.department'),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='phone',
            field=models.CharField(blank=True, max_length=45),
        ),
    ]
