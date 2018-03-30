from django.db import models

from prehab_app.models.Patient import Patient
from prehab_app.models.ConstraintType import ConstraintType


class PatientConstraintType(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    constraint_type = models.ForeignKey(ConstraintType, on_delete=models.CASCADE, db_column='constraint_type_id')

    class Meta:
        managed = False
        db_table = 'patient_constraint_type'
        ordering = ['-id']
