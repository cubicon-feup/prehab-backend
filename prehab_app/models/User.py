from django.db import models

from prehab_app.models.UserType import UserType


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False, null=True)
    email = models.CharField(max_length=64, blank=False, null=True)
    phone = models.CharField(max_length=64, blank=False, null=True)
    username = models.CharField(max_length=64, blank=False, null=False)
    password = models.CharField(max_length=64, blank=False, null=True)
    user_type_id = models.ForeignKey(UserType, on_delete=models.CASCADE, db_column='user_type_id')

    class Meta:
        managed = False
        db_table = 'users'
        ordering = ['-id']
