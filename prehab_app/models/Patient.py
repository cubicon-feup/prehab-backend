from django.db import models

from prehab_app.models.User import User


class Patient(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    patient_tag = models.CharField(max_length=16, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    height = models.FloatField(blank=False, null=False)
    weight = models.FloatField(blank=False, null=False)
    sex = models.CharField(max_length=1, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'patient'
        ordering = ['-id']
