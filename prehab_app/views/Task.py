from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab_app.models.Task import Task
from prehab_app.models.TaskType import TaskType
from prehab.permissions import Permission
from prehab_app.serializers.Task import TaskSerializer


class TaskViewSet(GenericViewSet):

    def list(self, request):
        queryset = self.paginate_queryset(Task.objects.all())
        data = TaskSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            task = Task.objects.get(pk=pk)

        except Task.DoesNotExist:
            return HTTP.response(404, 'Task with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        data = TaskSerializer(task, many=False).data
        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        try:
            if not Permission.verify(request, ['Admin']):
                raise HttpException(401)

            data = request.data
            # 1. Check schema
            SchemaValidator.validate_obj_structure(data, 'task/create.json')

            # 2. Check if task type is available
            task_type = TaskType.objects.task_type(data['task_type_id'])

            if len(task_type) == 0:
                raise HttpException(400, 'Task Type does not exist.')

            new_task = Task(
                title=data['title'],
                description=data.get('description', None),
                multimedia_link=data.get('multimedia_link', None),
                task_type=task_type.get()
            )
            new_task.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        data = {
            'task_id': new_task.id
        }
        return HTTP.response(201, '', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
