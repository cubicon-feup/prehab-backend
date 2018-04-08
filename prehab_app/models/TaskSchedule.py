from django.db import models

# from prehab_app.models.WeekTaskSchedule import WeekTaskSchedule
from prehab_app.models.TaskScheduleStatus import TaskScheduleStatus
from prehab_app.models.User import User


class TaskScheduleQuerySet(models.QuerySet):
    pass
    # def weeks(self, task_schedule_id):
    #     return WeekTaskSchedule.objects.filter('task_schedule_id', task_schedule_id)


class TaskSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=False)
    number_of_weeks = models.IntegerField(blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by')
    is_active = models.BooleanField(blank=False, default=True)
    status = models.ForeignKey(TaskScheduleStatus, on_delete=models.CASCADE, db_column='status_id', default=1)

    objects = TaskScheduleQuerySet.as_manager()

    class Meta:
        # app_label = 'TaskSchedule'
        # managed = False
        db_table = 'task_schedule'
        ordering = ['-id']
