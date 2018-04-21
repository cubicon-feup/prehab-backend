from prehab_app.models import User, Role
from prehab_app.tests.TestSuit import TestSuit


class UserViewTests(TestSuit):
    url_path = '/api/user/'

    def test_activation_of_user(self):
        user = User(
            name="Test name",
            email="user@email.pt",
            phone="123456789",
            username="username",
            role=Role.objects.get(pk=1),
            activation_code='12345',
            is_active=False
        )
        user.save()

        # ERROR - no parameters
        body = {}
        res = self.http_request('post', self.url_path + 'activate/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'You need to send activation code and password')

        # ERROR - missing required parameters
        body = {
            "activation_code": "12345"
        }
        res = self.http_request('post', self.url_path + 'activate/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'You need to send activation code and password')
        body = {
            "password": "pass"
        }
        res = self.http_request('post', self.url_path + 'activate/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'You need to send activation code and password')

        # ERROR - Invalid activation code
        body = {
            "activation_code": "xxxxx",
            "password": "test-password"
        }
        res = self.http_request('post', self.url_path + 'activate/', body)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()['details'], 'Invalid Activation Code.')

        # SUCCESS
        body = {
            "activation_code": "12345",
            "password": "password",
        }
        self.assertIsNone(user.password)
        res = self.http_request('post', self.url_path + 'activate/', body)
        user = User.objects.get(pk=user.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(user.is_active, True)
        self.assertTrue(user.password, 'password')

        # ERROR - user already active
        body = {
            "activation_code": "12345",
            "password": "password",
        }
        res = self.http_request('post', self.url_path + 'activate/', body)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()['details'], 'You are already active.')
