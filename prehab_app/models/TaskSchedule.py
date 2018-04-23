from django.db import models

# from prehab_app.models.WeekTaskSchedule import WeekTaskSchedule
from prehab_app.models.User import User


class TaskScheduleQuerySet(models.QuerySet):
    def created_by(self, doctor_id):
        return self.filter(created_by=doctor_id).all()


class TaskSchedule(models.Model):
    PENDING = 1
    ONGOING = 2
    COMPLETED = 3
    NOT_COMPLETED = 4

    Status = (
        (PENDING, 'Pending'),
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
        (NOT_COMPLETED, 'Not Completed'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=False)
    number_of_weeks = models.IntegerField(blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by')
    is_active = models.BooleanField(blank=False, default=True)
    status = models.IntegerField(choices=Status, default=PENDING)

    objects = TaskScheduleQuerySet.as_manager()

    class Meta:
        db_table = 'task_schedule'
        ordering = ['-id']

    def doctor_can_use(self, doctor_id):
        return self.created_by.is_admin or self.created_by.id == doctor_id
