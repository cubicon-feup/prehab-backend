from unittest import TestCase

from prehab_app.models.Role import Role
from prehab_app.models.User import User


class UserQuerySetTests(TestCase):
    def setUp(self):
        role = Role.objects.create(title='Admin for Tests')
        self.user = User.objects.create(name='Personal', username='admin', password='admin', role=role)

    def test_match_credentials_queryset(self):
        queryset = User.objects.match_credentials('admin', 'notadmin')
        self.assertEquals(queryset.count(), 0)
        queryset = User.objects.match_credentials('admin', 'admin')
        self.assertEquals(queryset.count(), 1)
        self.assertEquals(1, 1)
