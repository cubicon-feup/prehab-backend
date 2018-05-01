from django.db import models

from prehab_app.models import ConstraintType
from prehab_app.models.Meal import Meal


class MealConstraintTypeQuerySet(models.QuerySet):
    pass


class MealConstraintType(models.Model):
    id = models.AutoField(primary_key=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_column='meal_id', related_name='meal')
    constraint_type = models.ForeignKey(ConstraintType, on_delete=models.CASCADE, db_column='constraint_type_id', related_name='constraint_type')

    objects = MealConstraintTypeQuerySet.as_manager()

    class Meta:
        db_table = 'meal_constraint_type'
        ordering = ['-id']
