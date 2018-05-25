import datetime

from prehab_app.models import Prehab, Patient, Doctor
from prehab_app.tests.TestSuit import TestSuit


class AuthViewTests(TestSuit):
    patient_path_url = '/api/patient/'

    def test_retrieve_patient(self):
        # Test Delete
        res = self.http_request('get', self.patient_path_url + '3', auth_user='doctor')
        self.assertEqual(res.status_code, 200)

    def test_list_all_patients(self):
        # Test to pass
        res = self.http_request('get', self.patient_path_url, auth_user='admin')
        self.assertEqual(res.status_code, 200)

        # Test to pass
        res = self.http_request('get', self.patient_path_url, auth_user='doctor')
        self.assertEqual(res.status_code, 200)

        # Test to pass
        res = self.http_request('get', self.patient_path_url, auth_user='patient')
        self.assertEqual(res.status_code, 401)

    def test_register_patient(self):
        # Error in schema
        body = {}
        res = self.http_request('post', self.patient_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter age is a required property')

        body = {
            "age": 60
        }
        res = self.http_request('post', self.patient_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter height is a required property')

        body = {
            "age": 60,
            "height": 1.8,
            "weight": 80,
            "sex": "X",
            "constraints": "test"
        }
        res = self.http_request('post', self.patient_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. X is not one of [M, F]. Review: sex')

        body = {
            "email": None,
            "age": "60",
            "height": "1.8",
            "weight": "80",
            "sex": "M",
            "constraints": [1, 2, 3]
        }
        res = self.http_request('post', self.patient_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. 60 is not of type integer. Review: age')

        body = {
            "email": 3,
            "age": 60,
            "height": 1.8,
            "weight": 80,
            "sex": 60,
            "constraints": "test"
        }
        res = self.http_request('post', self.patient_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. 3 is not of type string, null. Review: email')

        # SUCCESS
        body = {
            "email": "x@x.x",
            "phone": None,
            "age": 60,
            "height": 1.8,
            "weight": 80,
            "sex": "M",
            "constraints": [1, 2, 3]
        }
        res = self.http_request('post', self.patient_path_url, body, auth_user='doctor')
        self.assertEqual(res.status_code, 201)

    def test_get_statistics(self):
        # Test Update
        res = self.http_request('get', self.patient_path_url + '3/statistics/', auth_user='admin')
        self.assertEqual(res.status_code, 400)

    def test_add_second_doctor(self):
        # Test to fail
        body = {
            "doctor_id": 100,
            "patient_id": 3
        }

        res = self.http_request('post', self.patient_path_url + 'add_second_doctor/', body, auth_user='admin')
        self.assertEqual(res.status_code, 404)

        # Test to fail
        body = {
            "doctor_id": 1,
            "patient_id": 7
        }

        res = self.http_request('post', self.patient_path_url + 'add_second_doctor/', body, auth_user='admin')
        self.assertEqual(res.status_code, 404)

        # Test Update
        body = {
            "doctor_id": 1,
            "patient_id": 3
        }

        res = self.http_request('post', self.patient_path_url + 'add_second_doctor/', body, auth_user='admin')
        self.assertEqual(res.status_code, 201)

    def test_update_patient(self):
        # Test Update
        res = self.http_request('put', self.patient_path_url, auth_user='patient')
        self.assertEqual(res.status_code, 405)

    def test_delete_patient(self):
        # Test Delete
        res = self.http_request('delete', self.patient_path_url, auth_user='patient')
        self.assertEqual(res.status_code, 405)
