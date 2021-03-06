from django.db import models


class RoleQuerySet(models.QuerySet):
    def which_role(self, role_id):
        return self.filter(pk=role_id)

    def admin_role(self):
        return self.filter(title='Admin')

    def doctor_role(self):
        return self.filter(title='Doctor')

    def patient_role(self):
        return self.filter(title='Patient')


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=True)
    description = models.CharField(max_length=512, blank=False, null=True)

    objects = RoleQuerySet.as_manager()

    class Meta:
        db_table = 'role'
        ordering = ['-id']

    def __str__(self):
        return self.title
