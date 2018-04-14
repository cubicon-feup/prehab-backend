from django.db import models

from prehab_app.models.Task import Task
from prehab_app.models.TaskSchedule import TaskSchedule


class ScheduleWeekTaskQuerySet(models.QuerySet):
    pass


class WeekTaskSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    task_schedule = models.ForeignKey(TaskSchedule, on_delete=models.CASCADE,
                                      db_column='task_schedule_id', related_name='week_task_schedule')
    week_number = models.IntegerField(blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='task_id', related_name='task')
    times_per_week = models.IntegerField(blank=False, null=False, default=1)
    repetition_number = models.IntegerField(blank=False, null=True, default=None)

    objects = ScheduleWeekTaskQuerySet.as_manager()

    class Meta:
        # app_label = 'ScheduleWeekTask'
        # managed = False
        db_table = 'week_task_schedule'
        ordering = ['-id']
