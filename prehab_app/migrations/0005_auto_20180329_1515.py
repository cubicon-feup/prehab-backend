# Generated by Django 2.0.2 on 2018-03-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prehab_app', '0004_auto_20180329_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
