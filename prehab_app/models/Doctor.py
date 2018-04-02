from django.db import models

from prehab_app.models.User import User


class Doctor(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    department = models.CharField(max_length=64, blank=False, null=True)

    class Meta:
        app_label = 'Doctor'
        managed = False
        db_table = 'doctor'
        ordering = ['-id']
