# Generated by Django 3.2.9 on 2021-12-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentmanagementapp', '0002_auto_20211206_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_date',
            field=models.DateField(),
        ),
    ]