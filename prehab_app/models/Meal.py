from django.db import models

from prehab_app.models.TaskType import TaskType


class MealQuerySet(models.QuerySet):
    pass


class Meal(models.Model):
    BREAKFAST = 1
    SNACK = 2
    FULL_MEAL = 3

    meal_types = (
        (BREAKFAST, 'Pequeno Almoço'),
        (SNACK, 'Lanche'),
        (FULL_MEAL, 'Refeição Completa')
    )
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)
    multimedia_link = models.CharField(max_length=512, blank=False, null=True)
    meal_type = models.IntegerField(choices=meal_types, default=SNACK)

    objects = MealQuerySet.as_manager()

    class Meta:
        db_table = 'meal'
        ordering = ['-id']
