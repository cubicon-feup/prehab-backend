from rest_framework.decorators import list_route
from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models import User
from prehab_app.models.Patient import Patient
from prehab.permissions import Permission
from prehab_app.serializers.Patient import PatientSerializer


class PatientViewSet(GenericViewSet):

    def list(self, request):
        try:
            # In case it's an Admin -> Retrieve ALL patients info
            if request.ROLE_ID == 1:
                queryset = self.paginate_queryset(Patient.objects.all())
            # In case it's a Doctor -> Retrieve ALL his/her patients info
            elif request.ROLE_ID == 2:
                queryset = self.paginate_queryset(Patient.objects.patients_of_doctor(request.ROLE_ID))
            # In case it's a Patient -> Retrieve info about that specific patient
            elif request.ROLE_ID == 3:
                return PatientViewSet.retrieve(request, request.USER_ID)
            else:
                raise HttpException(400, 'Some error occurred')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        data = PatientSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            patient = Patient.objects.get(id=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and request.USER_ID not in patient.which_doctor():
                raise HttpException(401, 'You don\t have permission to access this Patient Information')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID == patient.id:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')

            data = PatientSerializer(patient, many=False).data

        except Patient.DoesNotExist:
            return HTTP.response(404, 'Patient with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        return HTTP.response(405, '')
        # if not Permission.verify(request, ['Doctor']):
        #     raise HttpException(401)
        #
        # try:
        #     data = request.data
        #     # 1. Check if task_type is not null
        #     if 'task_type_id' not in data:
        #         raise HttpException(400, 'You need to send a task_type_id.')
        #
        #     # 2. Check if task type is available
        #     task_type = TaskType.objects.task_type(data['task_type_id'])
        #
        #     if len(task_type) == 0:
        #         raise HttpException(400, 'Task Type does not exist.')
        #
        #     new_task = Task(
        #         title=data['title'],
        #         description=data.get('description', None),
        #         multimedia_link=data.get('multimedia_link', None),
        #         task_type=task_type.get()
        #     )
        #     new_task.save()
        #
        # except HttpException as e:
        #     return HTTP.response(e.http_code, e.http_detail)
        # except Exception as e:
        #     return HTTP.response(400, str(e))
        #
        # # Send Response
        # data = {
        #     'task_id': new_task.id
        # }
        # return HTTP.response(201, '', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
