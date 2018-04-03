#!/usr/bin/python
import os
import re
import shutil
import subprocess

import psycopg2
import psycopg2.extras

SCHEMA = "public"
CONFIG = {
    "suppliers": [
        "user_type",
        "doctor",
        "patient_type",
        "patient",
        "doctor_patient",
        "prehab_status",
        "task_schedule",
        "task_type",
        "task_type_id",
        "schedule_week_task",
        "prehab_end_date",
        "task_schedule_status",
        "patient_task_schedule"
    ]
}


def snake_to_camel(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def camel_to_snake(word):
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()


def remove_file(path):
    if file_or_folder_exists(path):
        try:
            os.remove(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def remove_folder(path):
    if file_or_folder_exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print("Error: %s." % (str(e)))


def create_file_and_folders(path, name_of_file=''):
    if not file_or_folder_exists(path):
        os.makedirs(path)
    return open('{}/{}'.format(path, name_of_file), 'w+') if name_of_file != '' else None


def file_or_folder_exists(file_path):
    return os.path.exists(file_path)


def save_model(file_path, service_name, service_name_capitalized, db_attributes):
    content = """from django.db import models
{3}

class {1}(models.Model):
{2}

    class Meta:
        managed = False
        db_table = '{0}'
        ordering = ['-id']
""".format(service_name, service_name_capitalized, "\n".join(get_model_lines(db_attributes)),
           "\n".join(get_model_imports(db_attributes)))

    try:
        with open(file_path, "w+") as file:
            file.write(content)
    except Exception:
        return False

    return True


def get_model_imports(db_columns):
    imports = []

    for db_column in db_columns:
        # SEARCH EVERY SERVICE/models for this specific model
        if db_column['column_name'].startswith('fk_'):
            parent_table = snake_to_camel(
                re.sub('fk_', '', db_column['column_name']))

            for directory in os.listdir('./'):
                models_directory = './{}/models'.format(directory)
                if file_or_folder_exists(models_directory) and file_or_folder_exists(
                        '{}/{}.py'.format(models_directory, parent_table)):
                    imports.append('from {0}.models.{1} import {1}'.format(
                        directory, parent_table))
                    break

    return imports


def get_model_lines(db_columns):
    model_lines = []

    for db_column in db_columns:
        # For primary keys
        if db_column['column_name'].startswith('id'):
            model_lines.append('    {} = models.AutoField(primary_key=True)'.format(
                db_column['column_name']))

        # For foreign keys
        elif db_column['column_name'].endswith('_id'):
            parent_table = snake_to_camel(
                re.sub('fk_', '', db_column['column_name']))
            model_lines.append("    {0} = models.ForeignKey({1}, on_delete=models.CASCADE, db_column='{0}')".format(
                db_column['column_name'],
                parent_table))

        # For others keys
        else:
            default = None if db_column['column_default'] is None else db_column['column_default']
            tmp_data = {
                'max_length': None if db_column['character_maximum_length'] is None else db_column[
                    'character_maximum_length'],
                'blank': 'False',
                'null': 'True' if db_column['is_nullable'] == 'YES' else 'False',
                'default': snake_to_camel(default) if default == 'false' or default == 'true' else default,
                'unique': 'True' if db_column['constraint_name'] is not None and db_column['constraint_name'].endswith(
                    '_unique') else None
            }

            if db_column['data_type'] == 'integer':
                field_type = 'IntegerField'
            elif db_column['data_type'] == 'character varying':
                field_type = 'CharField'
            elif db_column['data_type'] == 'numeric':
                field_type = 'FloatField'
            elif db_column['data_type'] == 'boolean':
                field_type = 'BooleanField'
                tmp_data['null'] = None
            elif db_column['data_type'] == 'text':
                field_type = 'TextField'
            elif db_column['data_type'] == 'date':
                field_type = 'DateTimeField'
            else:
                continue

            column_attributes = ", ".join(
                [str(key) + '=' + str(value) for key, value in tmp_data.items() if value is not None])
            model_line = "    {} = models.{}({})".format(
                db_column['column_name'], field_type, column_attributes)

            model_lines.append(model_line)

    return model_lines


def save_serializer(file_path, app_name, service_name_capitalized):
    content = """from rest_framework import serializers

from {0}.models import {1}


class {1}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {1}
        fields = '__all__'
""".format(app_name, service_name_capitalized)

    try:
        with open(file_path, "w+") as file:
            file.write(content)
    except Exception:
        return False

    return True


def save_viewset(file_path, app_name, service_name, service_name_capitalized):
    content = """from masterdata_crud_api.HuubClasses.HuubView import HuubViewSet
from ..models.{2} import {2}
from ..serializers.{2} import {2}Serializer, {2}SerializerWithoutAuditory


class {2}ViewSet(HuubViewSet):

    def __init__(self):
        super().__init__({2}, {2}Serializer, {2}SerializerWithoutAuditory, '{0}/schemas/{1}/')
""".format(app_name, service_name, service_name_capitalized)

    try:
        with open(file_path, "w+") as file:
            file.write(content)
    except Exception:
        return False

    return True


def get_urls_config(service_name, service_name_capitalized):
    url_config = """
    url(r'{0}/(?P<obj_pk>\d+)',
        {1}ViewSet.as_view({{
            'get': 'get_one',
            'put': 'update_one',
            'delete': 'delete_one',
        }}),
        name='CRUD over one {1}'),
    url(r'{0}/',
        {1}ViewSet.as_view({{
            'get': 'get_multiple',
            'post': 'insert',
            'put': 'update_multiple',
            'delete': 'delete_multiple',
        }}),
        name='CRUD over multiple {1}'),

    """.format(service_name, service_name_capitalized)

    return url_config


def save_urls_file(file_path, urls_imports, urls_data):
    content = """from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

{}

router = DefaultRouter()

urlpatterns = [
    {}
    url(r'^', include(router.urls)),
]
""".format("\n".join(urls_imports), "\n".join(urls_data))

    try:
        with open(file_path, "w+") as file:
            file.write(content)
    except Exception:
        return False

    return True


def connect_to_db():
    db_host = "prehab-pg-db.c4sdnouwglfv.eu-west-2.rds.amazonaws.com"
    db_port = "5432"
    db_name = "prehab_db"
    db_user = "prehab_user"
    db_pass = "Vf1mzubPejW4RqrbL3cm"
    conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}' port='{4}'".format(
        db_host, db_name, db_user, db_pass, db_port)

    # get a connection, if a connect cannot be made an exception will be raised here
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
    except Exception:
        return None
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return cursor


def get_information_schema(cursor, table_name):
    query = """
    select cols.column_name, 
      cols.data_type, cols.is_nullable, cols.data_type, cols.character_maximum_length, cols.column_default, const.constraint_name
    from information_schema.columns cols
    left join information_schema.constraint_column_usage const on 
      const.column_name = cols.column_name and 
      const.table_name = cols.table_name and 
      const.table_schema = cols.table_schema
    where 
      cols.table_schema = '{}' and 
      cols.table_name = '{}' and 
      cols.column_name not in ('created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')
    order by cols.ordinal_position
    """.format(SCHEMA, table_name)

    cursor.execute(query)

    return cursor.fetchall()


def add_init_files(app_name):
    # Create Models init file if doesn't exist
    if not file_or_folder_exists('{}/models/__init__.py'.format(app_name)):
        create_file_and_folders('{}/models'.format(app_name), '__init__.py')

    # Create __init__ for serializer if doesn't exist
    if not file_or_folder_exists('{}/serializers/__init__.py'.format(app_name)):
        create_file_and_folders(
            '{}/serializers'.format(app_name), '__init__.py')

    # Create __init__ for viewset if doesn't exist
    if not file_or_folder_exists('{}/views/__init__.py'.format(app_name)):
        create_file_and_folders('{}/views'.format(app_name), '__init__.py')


def main():
    db_cursor = connect_to_db()

    for app_name, services in CONFIG.items():
        app_name_capitalized = snake_to_camel(app_name)

        print("Creating new app: {}".format(app_name_capitalized))

        # Create django app
        subprocess.call(
            "python manage.py startapp {}".format(app_name), shell=True)

        # Remove unnecessary files
        print("Removing unnecessary files")
        remove_file('{}/admin.py'.format(app_name))
        remove_file('{}/tests.py'.format(app_name))
        remove_file('{}/views.py'.format(app_name))
        remove_file('{}/models.py'.format(app_name))
        remove_folder('{}/migrations/'.format(app_name))

        # Add necessary folders and files
        print("Adding necessary files amd folders")
        create_file_and_folders('{}/models'.format(app_name), '__init__.py')
        create_file_and_folders(
            '{}/serializers'.format(app_name), '__init__.py')
        create_file_and_folders('{}/views'.format(app_name), '__init__.py')
        create_file_and_folders('{}/schemas'.format(app_name))

        urls_imports = []
        urls_data = []

        add_init_files(app_name)

        # Create urls file
        if not file_or_folder_exists('{}/urls.py'.format(app_name)):
            create_file_and_folders('{}'.format(app_name), 'urls.py')

        for service_name in services:
            db_attributes = get_information_schema(db_cursor, service_name)
            service_name_capitalized = snake_to_camel(service_name)

            print("Creating new service: {}".format(service_name_capitalized))

            # ******************************************
            # **                MODEL                 **
            # ******************************************

            # Substitute Model for entity
            remove_file('{}/models/{}'.format(app_name,
                                              service_name_capitalized))

            # Write init file for models
            with open('{}/models/__init__.py'.format(app_name), "a") as model_init_file:
                model_init_file.write("from .{} import {}\n".format(
                    service_name_capitalized, service_name_capitalized))

            save_model('{}/models/{}.py'.format(app_name, service_name_capitalized),
                       service_name, service_name_capitalized, db_attributes)

            # ******************************************
            # **             SERIALIZER               **
            # ******************************************

            # Substitute Serializer for entity
            remove_file('{}/serializers/{}'.format(app_name,
                                                   service_name_capitalized))

            # Create Serializer for entity if does not exist
            if not file_or_folder_exists('{}/serializers/{}'.format(app_name, service_name_capitalized)):
                save_serializer('{}/serializers/{}.py'.format(app_name,
                                                              service_name_capitalized), app_name,
                                service_name_capitalized)

            # ******************************************
            # **               VIEWSET                **
            # ******************************************

            # Substitute Serializer for entity
            remove_file('{}/views/{}'.format(app_name,
                                             service_name_capitalized))

            # Create Viewset for entity if does not exist
            if not file_or_folder_exists('{}/views/{}'.format(app_name, service_name_capitalized)):
                save_viewset('{}/views/{}.py'.format(app_name, service_name_capitalized),
                             app_name, service_name, service_name_capitalized)

            # ******************************************
            # **                 URLS                 **
            # ******************************************
            urls_imports.append("from {0}.views.{1} import {1}ViewSet".format(
                app_name, service_name_capitalized))
            urls_data.append(get_urls_config(
                service_name, service_name_capitalized))

            print('Success.\n')

        save_urls_file('{}/urls.py'.format(app_name), urls_imports, urls_data)

        print("{} App added with success.".format(app_name_capitalized))

        # subprocess.call('pip install autopep8')
        # subprocess.call('autopep8 ./ --recursive --in-place --pep8-passes 2000 --verbose --max-line-length 140')


main()
