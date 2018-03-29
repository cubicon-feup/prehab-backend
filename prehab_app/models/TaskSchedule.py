from django.db import models


class TaskSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    is_active = models.BooleanField(blank=False, default=True)

    class Meta:
        managed = False
        db_table = 'task_schedule'
        ordering = ['-id']
