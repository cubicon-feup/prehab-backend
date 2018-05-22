from django.db import models


class TaskQuerySet(models.QuerySet):
    pass


class Task(models.Model):
    RESPIRATORIO = 1
    ENDURANCE = 2
    MUSCULAR = 3

    type_of_tasks = (
        (RESPIRATORIO, 'Respiratório'),
        (ENDURANCE, 'Endurance'),
        (MUSCULAR, 'Muscular')
    )
    title = models.CharField(max_length=256, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)
    multimedia_link = models.CharField(max_length=512, blank=False, null=True)
    task_type = models.IntegerField(choices=type_of_tasks, db_column='task_type_id')

    objects = TaskQuerySet.as_manager()

    class Meta:
        db_table = 'task'
        ordering = ['-id']
