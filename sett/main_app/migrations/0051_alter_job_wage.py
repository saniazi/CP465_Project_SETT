# Generated by Django 3.2.3 on 2021-07-04 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0050_auto_20210703_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='wage',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]