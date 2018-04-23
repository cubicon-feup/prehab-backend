from django.db import models


class ConstraintTypeQuerySet(models.QuerySet):
    pass


class ConstraintType(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=512, blank=False, null=True)

    objects = ConstraintTypeQuerySet.as_manager()

    class Meta:
        db_table = 'constraint_type'
        ordering = ['-id']
