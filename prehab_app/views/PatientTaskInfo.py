from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab_app.models.Patient import Patient
from prehab_app.models.PatientTaskInfo import PatientTaskInfo
from prehab_app.serializers.PatientTaskInfo import PatientTaskInfoSerializer


class PatientTaskInfoViewSet(GenericViewSet):

    def list(self, request):
        """
        Query Parameters: patient_id
        :param request:
        :return:
        """
        try:
            if 'patient_id' in request.GET and request.GET.get('patient_id'):
                patient_task_info = PatientTaskInfo.objects.filter(patient=request.GET['patient_id'])
            else:
                patient_task_info = PatientTaskInfo.objects

            # In case it's an Admin -> Retrieve ALL PREHABS info
            if request.ROLE_ID == 1:
                patient_task_info = patient_task_info.all()
            # In case it's a Doctor -> Retrieve ALL plans created by him
            elif request.ROLE_ID == 2:
                patient_task_info = patient_task_info.filter(doctor=request.USER_ID).all()
            # In case it's a Patient -> Retrieve his plan
            elif request.ROLE_ID == 3:
                patient_task_info = patient_task_info.filter(patient=request.USER_ID).all()
            else:
                raise HttpException(400, 'Some error occurred')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        queryset = self.paginate_queryset(patient_task_info)
        data = PatientTaskInfoSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            patient_task_info = PatientTaskInfo.objects.get(pk=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and request.USER_ID == patient_task_info.doctor.id:
                raise HttpException(401, 'You don\t have permission to access this')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID == patient_task_info.patient.id:
                raise HttpException(401, 'You don\t have permission to access this')

            data = PatientTaskInfoSerializer(patient_task_info, many=False).data

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

    @staticmethod
    def update(request, pk=None):
        try:
            # 1. Check schema
            SchemaValidator.validate_obj_structure(request.data, 'patient_task_info/update.json')

            patient_task_info = PatientTaskInfo.objects.get(pk=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID != 2 or request.ROLE_ID == 2 and request.USER_ID == patient_task_info.doctor.id:
                raise HttpException(401, 'You don\t have permission to access this')

            patient_task_info.seen_by_doctor = request.data['seen']
            patient_task_info.doctor_notes = request.data['doctor_notes']
            patient_task_info.save()

        except PatientTaskInfo.DoesNotExist:
            return HTTP.response(404, 'Patient Task with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        return HTTP.response(200, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
