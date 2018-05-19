from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.permissions import Permission
from prehab_app.models import TaskSchedule
from prehab_app.serializers.TaskSchedule import TaskScheduleSerializer


class TaskScheduleViewSet(GenericViewSet):

    def list(self, request):
        try:
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

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            queryset = TaskSchedule.objects.get(pk=pk)
            data = TaskScheduleSerializer(queryset, many=True).data[0]

        except TaskSchedule.DoesNotExist:
            return HTTP.response(404, 'Patient with id {} does not exist'.format(str(pk)))
        except ValueError:
            return HTTP.response(404, 'Invalid url format. {}'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

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
