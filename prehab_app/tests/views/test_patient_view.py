from prehab_app.tests.TestSuit import TestSuit


class AuthViewTests(TestSuit):
    patient_path_url = '/api/patient/'

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
            "constraints": [1, 2, 3]
        }
        res = self.http_request('post', self.patient_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. X is not one of [M, F]. Review: sex')

        body = {
            "email": None,
            "age": "60",
            "height": 1.8,
            "weight": 80,
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
            "sex": "M",
            "constraints": [1, 2, 3]
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
        self.assertEqual(res.status_code, 200)
