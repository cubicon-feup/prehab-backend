from django.db import transaction
from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models import TaskSchedule, WeekTaskSchedule, Task, User
from prehab_app.serializers.TaskSchedule import FullTaskScheduleSerializer


class FullTaskScheduleViewSet(GenericViewSet):

    @staticmethod
    def list(request):
        return HTTP.response(405)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            # 0 - Handle Permissions
            if not Permission.verify(request, ['Admin', 'Doctor']):
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.',
                                    'You don\'t have access to this resource.')

            # Check if Task Schedule exists and if it's the owner requesting it
            task_schedule = TaskSchedule.objects.get(pk=pk)

            if request.ROLE_ID == 2 and task_schedule.created_by.id != request.USER_ID:
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.',
                                    'You don\'t have access to this resource.')

            data = FullTaskScheduleSerializer(instance=task_schedule).data

        except TaskSchedule.DoesNotExist:
            return HTTP.response(404, 'Plano de Tarefas não encontrado.',
                                 'Task Schedule with id {} not found.'.format(str(pk)))
        except ValueError:
            return HTTP.response(404, 'Url com formato inválido.', 'Invalid URL format. {}'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado',
                                 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, data=data)

    @staticmethod
    def create(request):
        try:
            # 0. Check Permissions
            if not Permission.verify(request, ['Admin', 'Doctor']):
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.',
                                    'You don\'t have access to this resource.')

            data = request.data
            # 1. Check schema
            SchemaValidator.validate_obj_structure(data, 'full_task_schedule/create.json')

            with transaction.atomic():
                # 2. Create Task Schedule
                task_schedule = TaskSchedule(
                    title=request.data['title'],
                    number_of_weeks=request.data['number_of_weeks'],
                    created_by=User.objects.get(pk=request.USER_ID),
                    is_active=True
                )

                task_schedule.save()

                # For Each Week, add them
                for week in request.data['weeks']:
                    week_number = week['week_number']
                    if 0 > week_number > request.data['number_of_weeks']:
                        raise HttpException(400, 'Número de semanas não eprmitida', 'Number of week is not allowed.')

                    for week_task in week['tasks']:
                        try:
                            task = Task.objects.get(pk=week_task['task_id'])
                        except Task.DoesNotExist:
                            raise HttpException(404,
                                                'Tarefa não enconbtrada',
                                                'Task with id {} does not exist.'.format(str(week_task['task_id'])))

                        schedule_week_task = WeekTaskSchedule(
                            task_schedule=task_schedule,
                            week_number=week_number,
                            task=task,
                            times_per_week=week_task['times_per_week'],
                            repetition_number=week_task.get('repetition_number', None)
                        )

                        schedule_week_task.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400,
                                 'Ocorreu um erro inesperado',
                                 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        data = {
            'task_schedule_id': task_schedule.id
        }

        return HTTP.response(201, 'Task Schedule criado com sucesso.', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405)

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405)
