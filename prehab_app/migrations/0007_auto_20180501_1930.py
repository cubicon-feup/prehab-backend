# Generated by Django 2.0.2 on 2018-05-01 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prehab_app', '0006_patientmealschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.IntegerField(choices=[(1, 'Respiratório'), (2, 'Endurance'), (3, 'Muscular')]),
        ),
        migrations.DeleteModel(
            name='TaskType',
        ),
    ]
