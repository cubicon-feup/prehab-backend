from rest_framework.test import APIRequestFactory

from prehab_app.tests.TestSuit import TestSuit
from prehab_app.views.Auth import AuthViewSet


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

    def test_new_logout(self):
        factory = APIRequestFactory()
        request = factory.get('/api/logout')
        # request = factory.get('/api/logout', args=(cat.pk,)))
        res = AuthViewSet.logout(request)
        self.assertEqual(res.status_code, 200)

    def test_register_patient(self):
        # Error in schema
        body = {}
        res = self.http_request('post', '/api/register_patient/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter age is a required property')

        body = {
            "age": 60
        }
        res = self.http_request('post', '/api/register_patient/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter height is a required property')

        body = {
            "age": 60,
            "height": 1.8
        }
        res = self.http_request('post', '/api/register_patient/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter weight is a required property')

        body = {
            "age": 60,
            "height": 1.8,
            "weight": 80
        }
        res = self.http_request('post', '/api/register_patient/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. Parameter constraints is a required property')

        # body = {
        #     "age": 60,
        #     "height": 1.8,
        #     "weight": 80,
        #     "constraints": [1, 2, 3]
        # }
        # res = self.http_request('post', '/api/register_patient/', body)
        # self.assertEqual(res.status_code, 400)
        # self.assertEqual(res.json()['details'], 'Validation Error. Parameter constraints is a required property')

        body = {
            "age": 60,
            "height": 1.8,
            "weight": 80,
            "sex": "X"
        }
        res = self.http_request('post', '/api/register_patient/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. X is not one of [M, F]. Review: sex')

        body = {
            "age": 60,
            "height": 1.8,
            "weight": 80,
            "sex": 60,
            "constraints": "test"
        }
        res = self.http_request('post', '/api/register_patient/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'Validation Error. 60 is not one of [M, F]. Review: sex')

        # body = {
        #     "email": None,
        #     "age": "60",
        #     "height": "1.8",
        #     "weight": "80",
        #     "sex": "M",
        #     "constraints": [1, 2, 3]
        # }
        # res = self.http_request('post', '/api/register_patient/', body)
        # self.assertEqual(res.status_code, 400)
        # self.assertEqual(res.json()['details'], 'Validation Error. Parameter constraints is a required property')

        # body = {
        #     "email": 3,
        #     "age": 60,
        #     "height": 1.8,
        #     "weight": 80,
        #     "sex": 60,
        #     "constraints": "test"
        # }
        # res = self.http_request('post', '/api/register_patient/', body)
        # self.assertEqual(res.status_code, 400)
        # self.assertEqual(res.json()['details'], 'Validation Error. Parameter constraints is a required property')

        # SUCCESS
        # body = {
        #     "email": "x@x.x",
        #     "phone": None,
        #     "age": 60,
        #     "height": 1.8,
        #     "weight": 80,
        #     "sex": "M",
        #     "constraints": [1, 2, 3]
        # }
        # res = self.http_request('post', '/api/register_patient/', body)
        # self.assertEqual(res.status_code, 400)
