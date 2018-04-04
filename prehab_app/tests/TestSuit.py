from django.test import TestCase

from prehab_app.models import User, Role


class TestSuit(TestCase):
    fixtures = ('constraint_types.json', 'prehab_status.json', 'roles.json', 'task_schedule_status.json', 'task_type.json', 'users.json')

    def setUp(self):
        self.admin_role = Role.objects.get(id=1)
        self.doctor_role = Role.objects.get(id=2)
        self.patient_role = Role.objects.get(id=3)

        self.admin_user = User.objects.get(id=1)
        self.doctor_user = User.objects.get(id=2)
        self.patient_user = User.objects.get(id=3)

    def http_request(self, method, url, body=None, auth_user = None, custom_headers=None):
        if not url.endswith('/'):
            url += '/'

        if auth_user in ('admin', 'Admin') or auth_user is None:
            body = {'username': 'admin', 'password': 'admin'}
        elif auth_user in ('doctor', 'Doctor'):
            body = {'username': 'doctor', 'password': 'doctor'}
        elif auth_user in ('patient', 'Patient'):
            body = {'username': 'patient', 'password': 'patient'}

        response = self.client.post('/api/login/', body)
        headers = {
            'HTTP_JWT': response.json()['data']['jwt']
        }

        if custom_headers is not None:
            headers = {**headers, **custom_headers}

        if body is None:
            body = dict()

        if method == 'get' or method == 'GET':
            response = self.client.get(url, **headers)
        elif method == 'post' or method == 'POST':
            response = self.client.post(url, body, **headers)
        elif method == 'put' or method == 'PUT':
            response = self.client.put(url, body, **headers)
        elif method == 'delete' or method == 'DELETE':
            response = self.client.delete(url, body, **headers)

        return response
