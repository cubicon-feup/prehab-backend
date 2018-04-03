from django.test import TestCase

from prehab_app.models import User, Role


class TestSuit(TestCase):
    fixtures = ('constraint_types.json', 'prehab_status.json', 'roles.json', 'task_schedule_status.json', 'task_type.json', 'users.json')

    def setUp(self):
        self.admin_role = Role.objects.get(id=1)
        self.doctor_role = Role.objects.get(id=2)
        self.patient_role = Role.objects.get(id=3)

        self.admin_user = User.objects.get(id=1)
        self.doctor_user = User.objects.get(id=2)
        self.patient_user = User.objects.get(id=3)
