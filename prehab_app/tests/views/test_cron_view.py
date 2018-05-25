import datetime

from prehab_app.models import Prehab, Patient, Doctor, PatientTaskSchedule
from prehab_app.tests.TestSuit import TestSuit


class AuthViewTests(TestSuit):
    login_path_url = '/api/cron/'

    def test_clean_tasks(self):
        # SUCCESS
        res = self.http_request('post', self.login_path_url + 'tasks/', {})
        self.assertEqual(res.status_code, 200)

    def test_clean_prehabs(self):
        # body = {
        #     "patient_id": 4,
        #     "init_date": "22-05-2017",
        #     "surgery_date": "06-06-2017",
        #     "task_schedule_id": 1
        # }
        # self.http_request('post', '/api/prehab/', body, 'admin')

        # SUCCESS
        res = self.http_request('post', self.login_path_url + 'prehabs/', {})
        self.assertEqual(res.status_code, 200)
