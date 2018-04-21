from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab_app.models.Notification import Notification
from prehab_app.models.Patient import Patient
from prehab_app.serializers.Notification import NotificationSerializer
from prehab_app.serializers.Patient import PatientSerializer


class PatientViewSet(GenericViewSet):

    def list(self, request):
        """
        Query Parameters: patient_id
        :param request:
        :return:
        """
        try:
            if 'patient_id' in request.GET and request.GET.get('patient_id'):
                notifications = Notification.objects.filter(patient=request.GET['patient_id'])
            else:
                notifications = Notification.objects

            # In case it's an Admin -> Retrieve ALL PREHABS info
            if request.ROLE_ID == 1:
                notifications = notifications.all()
            # In case it's a Doctor -> Retrieve ALL plans created by him
            elif request.ROLE_ID == 2:
                notifications = notifications.filter(created_by=request.USER_ID).all()
            # In case it's a Patient -> Retrieve his plan
            elif request.ROLE_ID == 3:
                notifications = notifications.filter(patient=request.USER_ID).all()
            else:
                raise HttpException(400, 'Some error occurred')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        queryset = self.paginate_queryset(notifications)
        data = NotificationSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            notification = Notification.objects.get(id=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and request.USER_ID == notification.doctor.id:
                raise HttpException(401, 'You don\t have permission to access this')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID == notification.patient.id:
                raise HttpException(401, 'You don\t have permission to access this')

            data = PatientSerializer(notification, many=False).data

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
            SchemaValidator.validate_obj_structure(request.data, 'notification/update.json')

            notification = Notification.objects.get(id=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID != 2 or request.ROLE_ID == 2 and request.USER_ID == notification.doctor.id:
                raise HttpException(401, 'You don\t have permission to access this')

            notification.seen = request.data['seen']
            notification.doctor_notes = request.data['doctor_notes']
            notification.save()

        except Patient.DoesNotExist:
            return HTTP.response(404, 'Patient with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        return HTTP.response(200, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
