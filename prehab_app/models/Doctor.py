from django.db import models

from prehab_app.models.User import User


class DoctorQuerySet(models.QuerySet):
    pass


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    department = models.CharField(max_length=64, blank=False, null=True)
    # patients = models.ManyToManyField(Patient)

    objects = DoctorQuerySet.as_manager()

    class Meta:
        db_table = 'doctor'
        ordering = ['-user_id']
