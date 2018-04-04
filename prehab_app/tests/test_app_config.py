from django.test import TestCase

from prehab_app.apps import PrehabAppConfig


class AppConfigTest(TestCase):
    def test(self):
        self.assertEqual(PrehabAppConfig.name, 'prehab_app')
        self.assertEqual(PrehabAppConfig.verbose_name, 'PreHab API')
