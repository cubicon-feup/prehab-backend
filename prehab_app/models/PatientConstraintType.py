from django.db import models

from prehab_app.models.Patient import Patient
from prehab_app.models.ConstraintType import ConstraintType


class PatientConstraintTypeQuerySet(models.QuerySet):
    pass


class PatientConstraintType(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', related_name='patient_constraints')
    constraint_type = models.ForeignKey(ConstraintType, on_delete=models.CASCADE, db_column='constraint_type_id')

    objects = PatientConstraintTypeQuerySet.as_manager()

    class Meta:
        db_table = 'patient_constraint_type'
        ordering = ['-id']
