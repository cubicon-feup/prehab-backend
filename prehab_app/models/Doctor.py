from django.db import models

from prehab_app.models.User import User


class Doctor(models.Model):
    id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='patient_type_id', primary_key=True)
    department = models.CharField(max_length=64, blank=False, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'
        ordering = ['-id']