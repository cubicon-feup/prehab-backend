from django.db import models


class PatientType(models.Model):
    diabeticos = 1
    renais = 2
    desnutridos = 3
    vegetarianos = 4
    hepáticos = 5
    hipertensos = 6
    normal = 7
    PATIENT_TYPE = (
        (diabeticos, "Diabéticos"),
        (renais, "Insuficientes Renais"),
        (desnutridos, "Desnutridos"),
        (vegetarianos, "vegetarianos"),
        (hipertensos, "hipertensos"),
        (normal, "Normal"),
    )
    type_of_patient = models.IntegerField(choices=PATIENT_TYPE, default=normal)
    description = models.CharField(max_length=50)

    class Meta:
        db_table = 'patient_type'