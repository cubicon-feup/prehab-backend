from django.db import models


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=64, blank=False, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'
        ordering = ['-id']
