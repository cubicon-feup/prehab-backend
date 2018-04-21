from prehab_app.tests.TestSuit import TestSuit


class DoctorViewTests(TestSuit):
    doctor_path_url = '/api/doctor/'

    def test_register_doctor(self):
        # Error in schema
        body = {}
        res = self.http_request('post', self.doctor_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter username is a required property')

        # Test for not string
        number_in_place_of_string = int(1234)
        body = {
            "username": number_in_place_of_string,
            "password": "validpasswordstring",
            "email": "valid@email.com"
        }
        res = self.http_request('post', self.doctor_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. 1234 is not of type string. Review: username')

        # Test for missing password
        body = {
            "username": "no_password_test"
        }
        res = self.http_request('post', self.doctor_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter password is a required property')

        # Test for missing email
        body = {
            "username": "no_email_test",
            "password": "no_email_test"
        }
        res = self.http_request('post', self.doctor_path_url, body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter email is a required property')

        # Test to pass - post
        body = {
            "username": "test_to_pass",
            "password": "test_to_pass",
            "email": "test_to_pass@mail.com"
        }
        res = self.http_request('post', self.doctor_path_url, body)
        self.assertEqual(res.status_code, 200)

        #####Test get

    def test_retrieve_doctor(self):
        # Fail with permission
        res = self.http_request('get', self.doctor_path_url + '2', auth_user='patient')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()['details'], 'You don\t have permission to access this Doctor Information')

        # Test to pass - get
        res = self.http_request('get', self.doctor_path_url + '2', auth_user='admin')
        self.assertEqual(res.status_code, 200)

    def test_update_doctor(self):
        ##### Test Update
        res = self.http_request('put', self.doctor_path_url + '2', auth_user='patient')
        self.assertEqual(res.status_code, 405)

    def test_delete_doctor(self):
        ##### Test Delete
        res = self.http_request('delete', self.doctor_path_url + '2', auth_user='patient')
        self.assertEqual(res.status_code, 405)
