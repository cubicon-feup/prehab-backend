from django.db import models

from prehab_app.models.TaskType import TaskType


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)
    multimedia_link = models.CharField(max_length=512, blank=False, null=True)
    task_type_id = models.ForeignKey(TaskType, on_delete=models.CASCADE, db_column='task_type_id')

    class Meta:
        managed = False
        db_table = 'task_schedule'
        ordering = ['-id']