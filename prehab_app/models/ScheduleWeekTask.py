from django.db import models

from prehab_app.models.Task import Task
from prehab_app.models.TaskSchedule import TaskSchedule


class ScheduleWeekTask(models.Model):
    id = models.AutoField(primary_key=True)
    task_schedule = models.ForeignKey(TaskSchedule, on_delete=models.CASCADE, db_column='task_schedule_id')
    week_number = models.IntegerField(blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='task_id')

    class Meta:
        app_label = 'ScheduleWeekTask'
        managed = False
        db_table = 'schedule_week_task'
        ordering = ['-id']
