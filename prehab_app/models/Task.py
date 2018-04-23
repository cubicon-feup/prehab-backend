from django.db import models

from prehab_app.models.TaskType import TaskType


class TaskQuerySet(models.QuerySet):
    pass


class Task(models.Model):
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)
    multimedia_link = models.CharField(max_length=512, blank=False, null=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, db_column='task_type_id')

    objects = TaskQuerySet.as_manager()

    class Meta:
        db_table = 'task'
        ordering = ['-id']
