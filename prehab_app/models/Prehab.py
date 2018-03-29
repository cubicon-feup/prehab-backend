from django.db import models

from prehab_app.models.PrehabStatus import PrehabStatus


class Prehab(models.Model):
    id = models.AutoField(primary_key=True)
    init_date = models.DateField(blank=False, null=False)
    expected_end_date = models.DateField(blank=False, null=False)
    actual_end_date = models.DateField(blank=False, null=False)
    surgery_date = models.DateField(blank=False, null=False)
    week_number = models.IntegerField(blank=False, null=False)
    status_id = models.ForeignKey(PrehabStatus, on_delete=models.CASCADE, db_column='status_id')

    class Meta:
        managed = False
        db_table = 'prehab_end_date'
        ordering = ['-id']
