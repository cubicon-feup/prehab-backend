from django.db import models

from prehab_app.models.Doctor import Doctor
from prehab_app.models.Patient import Patient


class DoctorPatient(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')

    class Meta:
        managed = False
        db_table = 'doctor_patient'
        ordering = ['-id']
