from django.db import models

from prehab_app.models.Meal import Meal
from prehab_app.models.Prehab import Prehab


class PatientMealScheduleQuerySet(models.QuerySet):
    pass


class PatientMealSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    prehab = models.ForeignKey(Prehab, on_delete=models.CASCADE, db_column='prehab_id', related_name='patient_meal_schedule')
    week_number = models.IntegerField(blank=False, null=False)
    day_number = models.IntegerField(blank=False, null=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_column='meal_id', related_name='patient_meal')

    objects = PatientMealScheduleQuerySet.as_manager()

    class Meta:
        db_table = 'patient_meal_schedule'
        ordering = ['-id']
