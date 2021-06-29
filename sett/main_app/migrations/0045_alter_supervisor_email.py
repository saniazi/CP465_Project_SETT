# Generated by Django 3.2.3 on 2021-06-29 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0044_auto_20210629_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email is already registered.'}, max_length=254, unique=True),
        ),
    ]
