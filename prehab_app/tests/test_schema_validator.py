from django.test import TestCase

from prehab.helpers.HttpException import HttpException
from prehab.helpers.SchemaValidator import SchemaValidator


class HttpResponseHandlerTest(TestCase):
    def test_validate_structure(self):
        body = {}
        try:
            self.assertRaises(HttpException, SchemaValidator.validate_obj_structure(body, 'test/test1.json'))
        except HttpException as e:
            self.assertEqual(e.http_code, 400)
            self.assertEqual(e.http_detail, 'Validation Error. Parameter required_string is a required property')

        body = {"required_string": "s", "max_len_string": "qwertyuiopasdfghjkl"}
        try:
            self.assertRaises(HttpException, SchemaValidator.validate_obj_structure(body, 'test/test1.json'))
        except HttpException as e:
            self.assertEqual(e.http_code, 400)
            self.assertEqual(e.http_detail, 'Validation Error. Parameter qwertyuiopasdfghjkl is too long')

        body = {"required_string": "s", "number": "dfgfgh"}
        try:
            self.assertRaises(HttpException, SchemaValidator.validate_obj_structure(body, 'test/test1.json'))
        except HttpException as e:
            self.assertEqual(e.http_code, 400)
            self.assertEqual(e.http_detail, 'Validation Error. dfgfgh is not of type number. Review: number')

        body = {"required_string": "s", "pattern": "4"}
        try:
            self.assertRaises(HttpException, SchemaValidator.validate_obj_structure(body, 'test/test1.json'))
        except HttpException as e:
            self.assertEqual(e.http_code, 400)
            self.assertEqual(e.http_detail, 'Validation Error. Parameter 4 does not match ^[1,2,3]$')

        body = {"required_string": "s"}
        self.assertEqual(SchemaValidator.validate_obj_structure(body, 'test/test1.json'), None)

        body = {"required_string": "s"}
        try:
            self.assertRaises(SchemaValidator.validate_obj_structure(body, 'test/test2.json'), Exception)
        except HttpException as e:
            self.assertEqual(e.http_code, 400)
            self.assertEqual(e.http_detail, 'File prehab_app/schemas/test/test2.json not found')
