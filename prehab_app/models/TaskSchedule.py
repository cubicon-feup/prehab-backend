from django.db import models

from prehab_app.models.Doctor import Doctor


class TaskScheduleQuerySet(models.QuerySet):
    pass


class TaskSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    is_active = models.BooleanField(blank=False, default=True)

    objects = TaskScheduleQuerySet.as_manager()

    class Meta:
        # app_label = 'TaskSchedule'
        # managed = False
        db_table = 'task_schedule'
        ordering = ['-id']
