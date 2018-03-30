from django.db import models


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)

    class Meta:
        managed = False
        db_table = 'role'
        ordering = ['-id']
