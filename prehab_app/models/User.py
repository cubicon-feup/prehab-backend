from django.db import models
from .TypeUser import TypeUser


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    typeUser = models.ForeignKey(TypeUser, on_delete=models.CASCADE, db_column='id')

    class Meta:
        db_table = 'auth_user'

