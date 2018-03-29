from django.db import models


class TypeUser(models.Model):
    fullAccess = 1
    doctorAccess = 2
    patientAccess = 3
    noAccess = 4
    PERMISSION = (
        (fullAccess, 'Full Access'),
        (doctorAccess, 'Doctor Permissions'),
        (patientAccess, 'Patient Permissions'),
        (noAccess, 'No Access')
    )
    type_of_user = models.IntegerField(choices=PERMISSION, default=noAccess)
    description = models.CharField(max_length=50)

    class Meta:
        db_table = 'type_user'
