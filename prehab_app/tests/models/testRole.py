from prehab_app.models import Role
from prehab_app.tests.testSuit import TestSuit


class RoleQuerySetTests(TestSuit):

    def test_which_role_queryset(self):
        queryset = Role.objects.which_role(10000)
        self.assertEqual(queryset.count(), 0)
        queryset = Role.objects.which_role(1)
        self.assertEquals(queryset.count(), 1)
        self.assertEquals(queryset.get().title, 'Admin')

    def test_admin_role_queryset(self):
        queryset = Role.objects.admin_role().get()
        self.assertEquals(queryset.id, 1)

    def test_doctor_role_queryset(self):
        queryset = Role.objects.doctor_role().get()
        self.assertEquals(queryset.id, 2)

    def test_patient_role_queryset(self):
        queryset = Role.objects.patient_role().get()
        self.assertEquals(queryset.id, 3)


class UserTests(TestSuit):
    def test_to_string_method(self):
        self.assertEquals(str(self.admin_role), 'Admin')
