from django.db import models

from prehab_app.models.Patient import Patient
from prehab_app.models.User import User
from prehab_app.models.PrehabStatus import PrehabStatus


class PrehabQuerySet(models.QuerySet):
    pass


class Prehab(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    init_date = models.DateField(blank=False, null=False)
    expected_end_date = models.DateField(blank=False, null=False)
    actual_end_date = models.DateField(blank=False, null=True, default=None)
    surgery_date = models.DateField(blank=False, null=False)
    number_of_weeks = models.IntegerField(blank=False, null=False)
    status = models.ForeignKey(PrehabStatus, on_delete=models.CASCADE, db_column='status_id')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by')

    objects = PrehabQuerySet.as_manager()

    class Meta:
        # app_label = 'Prehab'
        # managed = False
        db_table = 'prehab'
        ordering = ['-id']
