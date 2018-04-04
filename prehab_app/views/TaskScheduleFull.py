from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models import TaskSchedule
from prehab.permissions import Permission
from prehab_app.serializers.TaskSchedule import TaskScheduleSerializer


class TaskViewSet(GenericViewSet):

    def add_full_task_schedule(self, request):
        return HTTP.response(200, '', data=data, paginator=self.paginator)
