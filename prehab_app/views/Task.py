from rest_framework.viewsets import ViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models.Task import Task
from prehab_app.models.TaskType import TaskType
from prehab_app.permissions import Permission


class TaskViewSet(ViewSet):

    def list(self, request):
        # self.serializer_class = self.serializer_class
        # queryset = self.model.objects.all()
        return HTTP.response(200, '')

    def create(self, request):
        if not Permission.verify(request, ['Admin']):
            raise HttpException(401)

        try:
            data = request.data
            # 1. Check if title is not null
            if data['title'] is None:
                raise HttpException(400, 'You need to send a title.')

            # 2. Check if task type is available
            task_type = TaskType.objects.title(data['task_type_id'])

            if len(task_type) == 0:
                raise HttpException(400, 'Task Type does not exist.')

            t = Task(
                title=data['title'],
                description=data.get('description', None),
                multimedia_link=data.get('multimedia_link', None),
                task_type=task_type.get()
            )
            t.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        return HTTP.response(201, '')
