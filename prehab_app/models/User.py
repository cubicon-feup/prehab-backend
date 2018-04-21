from django.db import models

from prehab_app.models.Role import Role


class UserQuerySet(models.QuerySet):
    def match_credentials(self, username, password):
        return self.filter(username=username, password=password)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False, null=True)
    email = models.CharField(max_length=64, blank=False, null=True)
    phone = models.CharField(max_length=64, blank=False, null=True)
    username = models.CharField(max_length=64, blank=False, null=False)
    password = models.CharField(max_length=64, blank=False, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id', related_name='role')
    activation_code = models.CharField(max_length=8, blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False, default=False)

    objects = UserQuerySet.as_manager()

    class Meta:
        # app_label = 'User'
        db_table = 'users'
        ordering = ['-id']

    def __str__(self):
        return self.name

    @property
    def is_admin(self):
        return self.role.title == 'Admin'

    @property
    def is_doctor(self):
        return self.role.title == 'Doctor'

    @property
    def is_patient(self):
        return self.role.title == 'Patient'
