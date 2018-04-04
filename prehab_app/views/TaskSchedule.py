from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models import TaskSchedule
from prehab.permissions import Permission
from prehab_app.serializers.TaskSchedule import TaskScheduleSerializer


class TaskScheduleViewSet(GenericViewSet):

    def list(self, request):
        queryset = self.paginate_queryset(Task.objects.all())
        data = TaskScheduleSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = TaskSchedule.objects.filter(id=pk)
        if len(queryset) == 0:
            return HTTP.response(404, '')

        data = TaskScheduleSerializer(queryset, many=True).data[0]
        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        return HTTP.response(405, '')

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
