from django.db import models

from prehab_app.models import Doctor
from prehab_app.models.Patient import Patient
from prehab_app.models.PrehabStatus import PrehabStatus


class PrehabQuerySet(models.QuerySet):
    pass


class Prehab(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', related_name='prehab_patient')
    init_date = models.DateField(blank=False, null=False)
    expected_end_date = models.DateField(blank=False, null=False)
    actual_end_date = models.DateField(blank=False, null=True, default=None)
    surgery_date = models.DateField(blank=False, null=False)
    number_of_weeks = models.IntegerField(blank=False, null=False)
    status = models.ForeignKey(PrehabStatus, on_delete=models.CASCADE, db_column='status_id')
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='created_by')

    objects = PrehabQuerySet.as_manager()

    class Meta:
        db_table = 'prehab'
        ordering = ['-id']
