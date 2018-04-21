from prehab_app.tests.TestSuit import TestSuit
from prehab_app.models.Patient import Patient
from prehab_app.models import Role, User
from datetime import datetime


class PrehabViewTests(TestSuit):
    prehab_path_url = '/api/prehab/'

    def test_register_prehab(self):
        # Error in schema
        body = {}
        res = self.http_request('post', self.prehab_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter patient_id is a required property')

        ## Test for init_date
        body = {
            "patient_id": 1
        }
        res = self.http_request('post', self.prehab_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter init_date is a required property')

        ## Test for wrong init_date
        body = {
            "patient_id": 1,
            "init_date": 2,
            "surgery_date": "3",
            "task_schedule_id": 1
        }
        res = self.http_request('post', self.prehab_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. 2 is not of type string. Review: init_date')

        ## Test for unexisting patient
        body = {
            "patient_id": 1,
            "init_date": "2",
            "surgery_date": "3",
            "task_schedule_id": 1
        }
        res = self.http_request('post', self.prehab_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Patient with id of 1 does not exist.')

    def test_update_prehab(self):
        ##### Test Update
        res = self.http_request('put', self.prehab_path_url + '0', auth_user='patient')
        self.assertEqual(res.status_code, 405)

    def test_delete_prehab(self):
        ##### Test Delete
        res = self.http_request('delete', self.prehab_path_url + '0', auth_user='patient')
        self.assertEqual(res.status_code, 405)
