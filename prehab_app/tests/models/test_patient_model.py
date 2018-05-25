from prehab_app.models import Patient
from prehab_app.tests.TestSuit import TestSuit


class PatientTests(TestSuit):
    def test_to_string_method(self):
        patient = Patient.objects.get(pk=self.patient_user.pk)
        self.assertEquals(str(patient), 'TAG')
