# Generated by Django 2.0.2 on 2018-04-29 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prehab_app', '0004_meal_mealconstrainttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='title',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
