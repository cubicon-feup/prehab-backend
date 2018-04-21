from django.db import models

from prehab_app.models.User import User


class PatientQuerySet(models.QuerySet):
    pass


class Patient(models.Model):
    # id = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id', primary_key=True)
    patient_tag = models.CharField(max_length=16, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    height = models.FloatField(blank=False, null=False)
    weight = models.FloatField(blank=False, null=False)
    sex = models.CharField(max_length=1, blank=False, null=False)

    objects = PatientQuerySet.as_manager()

    class Meta:
        # app_label = 'Patient'
        # managed = False
        db_table = 'patient'
        ordering = ['-user_id']

    def __str__(self):
        return self.patient_tag

    # def doctor(self):
    #     return DoctorPatient.objects.filter(patient_id=self.id).values_list('doctor', flat=True)
