# Generated by Django 3.2.3 on 2021-06-26 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0035_auto_20210626_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.TextField(max_length=200),
        ),
    ]
