import json

from prehab_app.models import User, Role
from django.test import TestCase, Client


class TestSuit(TestCase):
    fixtures = ('constraint_types.json', 'prehab_status.json', 'roles.json', 'task_schedule_status.json', 'task_type.json', 'users.json')

    def setUp(self):
        self.client = Client()

        self.admin_role = Role.objects.get(id=1)
        self.doctor_role = Role.objects.get(id=2)
        self.patient_role = Role.objects.get(id=3)

        self.admin_user = User.objects.get(id=1)
        self.doctor_user = User.objects.get(id=2)
        self.patient_user = User.objects.get(id=3)

        self.admin_jwt = self.get_jwt_from_login('admin', 'admin')
        self.doctor_jwt = self.get_jwt_from_login('doctor', 'doctor')
        self.patient_jwt = self.get_jwt_from_login('patient', 'patient')

    def get_jwt_from_login(self, username, password):
        return self.client.post('/api/login/', {'username': username, 'password': password}).json()['data']['jwt']

    def http_request(self, method, url, body=None, auth_user=None, custom_headers=None, custom_auth=None):
        if not url.endswith('/'):
            url += '/'

        headers = {}

        if auth_user in ('admin', 'Admin') or auth_user is None:
            headers = {'HTTP_JWT': self.admin_jwt}
        elif auth_user in ('doctor', 'Doctor'):
            headers = {'HTTP_JWT': self.doctor_jwt}
        elif auth_user in ('patient', 'Patient'):
            headers = {'HTTP_JWT': self.patient_jwt}

        if custom_auth is not None:
            jwt = self.get_jwt_from_login(custom_auth['username'], custom_auth['password'])
            headers = {'HTTP_JWT': jwt}

        if custom_headers is not None:
            headers = {**headers, **custom_headers}

        if body is None:
            body = dict()

        if method == 'get' or method == 'GET':
            response = self.client.get(url, **headers)
        elif method == 'post' or method == 'POST':
            response = self.client.post(url, json.dumps(body), **headers, format='json', content_type='application/json')
        elif method == 'put' or method == 'PUT':
            response = self.client.put(url, json.dumps(body), **headers, format='json', content_type='application/json')
        elif method == 'delete' or method == 'DELETE':
            response = self.client.delete(url, json.dumps(body), **headers, format='json', content_type='application/json')
        else:
            response = None

        return response
