from prehab_app.tests.TestSuit import TestSuit


class FullTaskViewTests(TestSuit):
    full_patient_task_schedule_path_url = '/api/patient/schedule/task/'

    def test_retrieve_patient_task_schedule(self):
        # Test Delete
        res = self.http_request('get', self.full_patient_task_schedule_path_url + '1', auth_user='patient')
        self.assertEqual(res.status_code, 200)

    def test_list_all_patient_task_schedules(self):
        # Test to pass
        res = self.http_request('get', self.full_patient_task_schedule_path_url, auth_user='admin')
        self.assertEqual(res.status_code, 200)

        # Test to pass
        res = self.http_request('get', self.full_patient_task_schedule_path_url, auth_user='doctor')
        self.assertEqual(res.status_code, 200)

        # Test to pass
        res = self.http_request('get', self.full_patient_task_schedule_path_url, auth_user='patient')
        self.assertEqual(res.status_code, 200)

    def test_mark_as_done(self):
        # Test Update
        body = {
            "patient_task_schedule_id": 16,
            "completed": True,
            "difficulties": True,
            "notes": "Doi me as costas"
        }
        res = self.http_request('put', self.full_patient_task_schedule_path_url + 'done/', body, auth_user='patient')
        self.assertEqual(res.status_code, 200)

    def test_mark_as_seen(self):
        # Test Update
        body = {
            "prehab_id": 1
        }
        res = self.http_request('put', '/api/patient/schedule/seen/bulk/', body, auth_user='doctor')
        self.assertEqual(res.status_code, 200)

    def test_update_patient_task_schedule(self):
        # Test Update
        res = self.http_request('put', self.full_patient_task_schedule_path_url + '1', auth_user='patient')
        self.assertEqual(res.status_code, 405)

    def test_delete_patient_task_schedule(self):
        # Test Delete
        res = self.http_request('delete', self.full_patient_task_schedule_path_url + '1', auth_user='patient')
        self.assertEqual(res.status_code, 405)
