from django.db import models

from prehab_app.models.PatientTaskScheduleStatus import PatientTaskScheduleStatus
from prehab_app.models.Prehab import Prehab
from prehab_app.models.Task import Task


class PatientTaskScheduleQuerySet(models.QuerySet):
    pass


class PatientTaskSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    prehab = models.ForeignKey(Prehab, on_delete=models.CASCADE, db_column='prehab_id', related_name='patient_task_schedule')
    week_number = models.IntegerField(blank=False, null=False)
    day_number = models.IntegerField(blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='task_id', related_name='patient_task')
    expected_repetitions = models.IntegerField(blank=False, null=True)
    actual_repetitions = models.IntegerField(blank=False, null=True)
    status = models.ForeignKey(PatientTaskScheduleStatus, on_delete=models.CASCADE, db_column='status_id')
    finished_date = models.DateField(blank=False, null=True, default=None, db_column='finished_date')

    was_difficult = models.BooleanField(blank=False, null=False, default=False)
    patient_notes = models.CharField(max_length=256, blank=False, null=True, default="")
    seen_by_doctor = models.BooleanField(blank=False, null=False, default=False)
    doctor_notes = models.CharField(max_length=256, blank=False, null=True, default="")

    objects = PatientTaskScheduleQuerySet.as_manager()

    class Meta:
        db_table = 'patient_task_schedule'
        ordering = ['-id']
