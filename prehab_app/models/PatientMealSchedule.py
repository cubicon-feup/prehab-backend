from django.db import models

from prehab_app.models.Meal import Meal
from prehab_app.models.Prehab import Prehab


class PatientMealScheduleQuerySet(models.QuerySet):
    pass


class PatientMealSchedule(models.Model):
    BREAKFAST = 1
    MORNING_SNACK = 2
    LUNCH = 3
    AFTERNOON_SNACK = 4
    DINNER = 5

    order_of_meals = (
        (BREAKFAST, 'Pequeno Almoço'),
        (MORNING_SNACK, 'Lanche da Manhã'),
        (LUNCH, 'Almoço'),
        (AFTERNOON_SNACK, 'Lanche da Tarde'),
        (DINNER, 'Jantar')
    )
    id = models.AutoField(primary_key=True)
    prehab = models.ForeignKey(Prehab, on_delete=models.CASCADE, db_column='prehab_id', related_name='patient_meal_schedule')
    week_number = models.IntegerField(blank=False, null=False)
    day_number = models.IntegerField(blank=False, null=False)
    meal_order = models.IntegerField(choices=order_of_meals, default=BREAKFAST)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_column='meal_id', related_name='patient_meal')

    objects = PatientMealScheduleQuerySet.as_manager()

    class Meta:
        db_table = 'patient_meal_schedule'
        ordering = ['-id']
