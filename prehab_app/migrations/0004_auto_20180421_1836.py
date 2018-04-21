# Generated by Django 2.0.2 on 2018-04-21 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prehab_app', '0003_auto_20180421_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patienttaskschedule',
            name='doctor_notes',
        ),
        migrations.RemoveField(
            model_name='patienttaskschedule',
            name='patient_notes',
        ),
        migrations.RemoveField(
            model_name='patienttaskschedule',
            name='seen_by_doctor',
        ),
        migrations.RemoveField(
            model_name='patienttaskschedule',
            name='was_difficult',
        ),
        migrations.AddField(
            model_name='patienttaskschedule',
            name='actuall_repetitions',
            field=models.IntegerField(null=True),
        ),
    ]
