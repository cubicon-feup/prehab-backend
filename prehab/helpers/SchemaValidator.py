import json

import jsonschema

from prehab.helpers.HttpException import HttpException


class SchemaValidator:

    @staticmethod
    def validate_obj_structure(req_json, file_path):
        try:
            with open('prehab_app/schemas/' + file_path, encoding='utf-8') as data_file:
                schema = json.loads(data_file.read())
            jsonschema.validate(req_json, schema)

        except jsonschema.SchemaError as e:
            raise HttpException(400, e.message)

        except jsonschema.ValidationError as e:
            if e.validator == 'pattern':
                detail = "Validation Error. {}. Review: {}".format(
                    e.message, ' -> '.join(map(str, e.absolute_path)))
            else:
                detail = "Validation Error. {}".format(
                    SchemaValidator.get_error_message(e))
            raise HttpException(400, detail)

        except AttributeError as e:
            raise HttpException(400, str(e))

        except Exception as e:
            raise HttpException(400, str(e))

        return None

    @staticmethod
    def get_error_message(exception):
        detail = "{0}. Review:".format(exception.message)
        for idx, path in enumerate(exception.absolute_path):
            if idx == 0:
                detail = "{0} {1}".format(detail, path)
            elif type(path).__name__ == 'str':
                detail = "{0} > {1} ".format(detail, path)
            elif type(path).__name__ == 'int':
                detail = "{0} (position: {1}) ".format(detail, path)
        return detail
