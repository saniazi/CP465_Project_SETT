# Generated by Django 3.2.3 on 2021-07-09 23:07

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0063_alter_student_id_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(default='profile_pics/default.png', upload_to=main_app.models.user_directory_path),
        ),
    ]
