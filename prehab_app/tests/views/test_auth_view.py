from prehab_app.tests.TestSuit import TestSuit
from prehab_app.views.Auth import AuthViewSet


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
