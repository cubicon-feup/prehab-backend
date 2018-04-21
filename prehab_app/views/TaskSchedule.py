from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.permissions import Permission
from prehab_app.models import TaskSchedule
from prehab_app.serializers.TaskSchedule import TaskScheduleSerializer


class TaskScheduleViewSet(GenericViewSet):

    def list(self, request):
        # 0. Check Permissions
        if not Permission.verify(request, ['Admin', 'Doctor']):
            raise HttpException(401)

        # In case it's an Admin -> Retrieve ALL patients info
        if request.ROLE_ID == 1:
            queryset = self.paginate_queryset(TaskSchedule.objects.all())
        # In case it's a Doctor -> Retrieve ALL his/her task schedules info
        elif request.ROLE_ID == 2:
            queryset = self.paginate_queryset(TaskSchedule.objects.created_by(request.USER_ID))
        else:
            raise HttpException(400, 'Some error occurred')

        data = TaskScheduleSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = TaskSchedule.objects.filter(pk=pk)
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
