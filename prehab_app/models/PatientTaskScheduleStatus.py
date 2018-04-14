from django.db import models


class PatientTaskScheduleStatusQuerySet(models.QuerySet):
    def pending(self):
        return self.get(id=1)

    def ongoing(self):
        return self.get(id=2)

    def completed(self):
        return self.get(id=3)

    def not_completed(self):
        return self.get(id=4)


class PatientTaskScheduleStatus(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)

    objects = PatientTaskScheduleStatusQuerySet.as_manager()

    class Meta:
        # app_label = 'TaskScheduleStatus'
        # managed = False
        db_table = 'patient_task_schedule_status'
        ordering = ['id']
