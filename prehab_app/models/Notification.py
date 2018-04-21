from django.db import models

from prehab_app.models.Doctor import Doctor
from prehab_app.models.Patient import Patient


class NotificationQuerySet(models.QuerySet):
    pass
    # def is_a_match(self, doctor_id, patient_id):
    #     count = self.filter(doctor=doctor_id).filter(patient=patient_id).count()
    #     return count == 1


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    description = models.CharField(max_length=256, blank=False, null=False)
    seen = models.BooleanField(default=False)
    doctor_notes = models.CharField(max_length=256, blank=False, null=True)

    objects = NotificationQuerySet.as_manager()

    class Meta:
        # app_label = 'DoctorPatient'
        # managed = False
        db_table = 'notification'
        ordering = ['-id']