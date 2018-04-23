from django.db import models

from prehab_app.models import Doctor
from prehab_app.models.Patient import Patient


class PrehabQuerySet(models.QuerySet):
    pass


class Prehab(models.Model):
    PENDING = 1
    ONGOING = 2
    COMPLETED = 3
    NOT_COMPLETED = 4

    Status = (
        (PENDING, 'Pending'),
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
        (NOT_COMPLETED, 'Not Completed'),
    )

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id', related_name='prehab_patient')
    init_date = models.DateField(blank=False, null=False)
    expected_end_date = models.DateField(blank=False, null=False)
    actual_end_date = models.DateField(blank=False, null=True, default=None)
    surgery_date = models.DateField(blank=False, null=False)
    number_of_weeks = models.IntegerField(blank=False, null=False)
    status = models.IntegerField(choices=Status, default=PENDING)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='created_by')

    objects = PrehabQuerySet.as_manager()

    class Meta:
        db_table = 'prehab'
        ordering = ['-id']
