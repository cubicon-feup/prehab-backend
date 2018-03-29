from django.db import models
from .User import User


class Doctor(models.Model):
    department = models.CharField(max_length=50)
    doctor_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, db_column='id')

    class Meta:
        db_table = 'doctor'
