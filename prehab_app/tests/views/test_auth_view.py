from prehab_app.tests.TestSuit import TestSuit


class AuthViewTests(TestSuit):
    login_path_url = '/api/login/'

    def test_login(self):
        # ERROR - test Login without body parameters
        res = self.client.post(self.login_path_url)
        self.assertEqual(res.status_code, 400)

        # ERROR - test Login with wrong body parameters
        body = {'username': 'doctor'}
        request = self.client.post(self.login_path_url, body)
        self.assertEqual(request.status_code, 400)
        body = {'password': 'doctor'}
        request = self.client.post(self.login_path_url, body)
        self.assertEqual(request.status_code, 400)

        # ERROR - test Login with right body parameters but wrong match
        body = {'username': 'doctor', 'password': 'patient'}
        request = self.client.post(self.login_path_url, body)
        self.assertEqual(request.status_code, 401)

        # SUCCESS
        body = {'username': 'doctor', 'password': 'doctor'}
        request = self.client.post(self.login_path_url, body)
        self.assertEqual(request.status_code, 200)
        # assert structure of response
        self.assertTrue('data' in request.json())
        self.assertTrue('jwt' in request.json()['data'])
        self.assertTrue('role' in request.json()['data'])
        # assert role name
        self.assertEqual(request.json()['data']['role'], 'Doctor')

    def test_logout(self):
        res = self.http_request('post', '/api/logout/')
        self.assertEqual(res.status_code, 200)
