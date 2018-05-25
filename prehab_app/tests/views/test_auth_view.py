import datetime

from prehab_app.models import Prehab, Patient, Doctor
from prehab_app.tests.TestSuit import TestSuit


class AuthViewTests(TestSuit):
    login_path_url = '/api/login/'

    def test_login(self):
        # ERROR - test Login with invalid platform
        res = self.http_request('post', self.login_path_url, platform='xpto')
        self.assertEqual(res.status_code, 403)

        # ERROR - test Login without body parameters
        res = self.http_request('post', self.login_path_url)
        self.assertEqual(res.status_code, 400)

        # ERROR - test Login with wrong body parameters
        body = {'username': 'doctor'}
        res = self.http_request('post', self.login_path_url, body)
        self.assertEqual(res.status_code, 400)
        body = {'password': 'doctor'}
        res = self.http_request('post', self.login_path_url, body)
        self.assertEqual(res.status_code, 400)

        # ERROR - test Login with right body parameters but wrong match
        body = {'username': 'doctor', 'password': 'patient'}
        res = self.http_request('post', self.login_path_url, body)
        self.assertEqual(res.status_code, 401)

        # ERROR - test Login with right body parameters but wrong match
        body = {'username': 'doctor', 'password': 'doctor'}
        res = self.http_request('post', self.login_path_url, body, platform='mobile')
        self.assertEqual(res.status_code, 401)

        # SUCCESS - With Prehab
        Prehab(
            patient=Patient.objects.get(pk=3),
            init_date=datetime.date.today(),
            expected_end_date=datetime.date.today(),
            surgery_date=datetime.date.today(),
            number_of_weeks=4,
            created_by=Doctor.objects.get(pk=2)
        ).save()
        body = {'username': 'patient', 'password': 'patient'}
        res = self.http_request('post', self.login_path_url, body, platform='mobile')
        self.assertEqual(res.status_code, 200)
        self.assertTrue('prehab_id' in res.json()['data'])

        # SUCCESS
        body = {'username': 'doctor', 'password': 'doctor'}
        res = self.http_request('post', self.login_path_url, body)
        self.assertEqual(res.status_code, 200)
        # assert structure of response
        self.assertTrue('data' in res.json())
        self.assertTrue('jwt' in res.json()['data'])
        self.assertTrue('role' in res.json()['data'])
        # assert role name
        self.assertEqual(res.json()['data']['role'], 'Doctor')

    def test_logout(self):
        res = self.http_request('post', '/api/logout/')
        self.assertEqual(res.status_code, 200)
