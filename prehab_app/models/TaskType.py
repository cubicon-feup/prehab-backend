from django.db import models


class TaskTypeQuerySet(models.QuerySet):

    def title(self, task_type_id):
        return self.filter(id=task_type_id)


class TaskType(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)

    objects = TaskTypeQuerySet.as_manager()

    class Meta:
        # app_label = 'TaskType'
        db_table = 'task_type'
        ordering = ['-id']
