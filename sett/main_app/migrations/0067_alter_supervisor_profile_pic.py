# Generated by Django 3.2.3 on 2021-07-20 18:53

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0066_auto_20210716_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='profile_pic',
            field=models.ImageField(default='../static/main_app/images/default.png', upload_to=main_app.models.user_directory_path),
        ),
    ]
