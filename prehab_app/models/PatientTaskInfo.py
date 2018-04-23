from django.db import models

from prehab_app.models.Doctor import Doctor
from prehab_app.models.Patient import Patient
from prehab_app.models.PatientTaskSchedule import PatientTaskSchedule


class PatientTaskInfoQuerySet(models.QuerySet):
    pass
    # def is_a_match(self, doctor_id, patient_id):
    #     count = self.filter(doctor=doctor_id).filter(patient=patient_id).count()
    #     return count == 1


class PatientTaskInfo(models.Model):
    id = models.AutoField(primary_key=True)
    patient_task = models.ForeignKey(PatientTaskSchedule, on_delete=models.CASCADE, db_column='patient_task_schedule_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    was_difficult = models.BooleanField(default=False)
    patient_notes = models.CharField(max_length=256, blank=False, null=False)
    seen_by_doctor = models.BooleanField(default=False)
    doctor_notes = models.CharField(max_length=256, blank=False, null=True)

    objects = PatientTaskInfoQuerySet.as_manager()

    class Meta:
        db_table = 'patient_task_info'
        ordering = ['-id']
