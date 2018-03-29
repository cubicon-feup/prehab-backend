from django.db import models
from .Doctor import Doctor
from .Patient import Patient


class ListDoctorPatient(models.Model):
    id_user = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
