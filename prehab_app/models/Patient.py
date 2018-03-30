from django.db import models

from prehab_app.models.PatientType import PatientType
from prehab_app.models.User import User


class Patient(models.Model):
    id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='patient_type_id', primary_key=True)
    patient_tag = models.CharField(max_length=16, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    sex = models.CharField(max_length=1, blank=False, null=False)
    patient_type_id = models.ForeignKey(PatientType, on_delete=models.CASCADE, db_column='patient_type_id')

    class Meta:
        managed = False
        db_table = 'patient'
        ordering = ['-id']
