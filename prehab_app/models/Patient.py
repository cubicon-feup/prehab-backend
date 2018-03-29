from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .PatientType import PatientType
from .User import User


class Patient(models.Model):
    male = "m"
    female = "f"
    SEX_TYPE = (
        (male, 'Male'),
        (female, 'Female')
    )
    tag = models.CharField(max_length=50, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sex = models.CharField(max_length=1, choices=SEX_TYPE, default=male)
    typePatient = models.ForeignKey(PatientType, on_delete=models.CASCADE, db_column='id')
    patient_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, default=1, db_column='id')

    class Meta:
        db_table = 'patient'