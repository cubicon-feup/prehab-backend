from prehab_app.models.User import User
from prehab_app.tests.TestSuit import TestSuit


class UserTests(TestSuit):
    def test_to_string_method(self):
        self.assertEquals(str(self.admin_user), 'Admin')

    def test_is_admin_method(self):
        self.assertEquals(self.admin_user.is_admin, True)
        self.assertEquals(self.admin_user.is_doctor, False)
        self.assertEquals(self.admin_user.is_patient, False)

    def test_is_doctor_method(self):
        self.assertEquals(self.doctor_user.is_admin, False)
        self.assertEquals(self.doctor_user.is_doctor, True)
        self.assertEquals(self.doctor_user.is_patient, False)

    def test_is_patient_method(self):
        self.assertEquals(self.patient_user.is_admin, False)
        self.assertEquals(self.patient_user.is_doctor, False)
        self.assertEquals(self.patient_user.is_patient, True)
