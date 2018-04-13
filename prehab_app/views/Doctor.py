from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models.Doctor import Doctor
from prehab_app.models.User import User
from prehab_app.serializers.Doctor import DoctorSerializer


class DoctorViewSet(GenericViewSet):

    def list(self, request):
        try:
            # In case it's an Admin and Doctors(need confirmation[security reasons]) -> Retrieve ALL doctors info
            if request.ROLE_ID == 1 and request.ROLE_ID == 2:
                queryset = self.paginate_queryset(Doctor.objects.all())
            else:
                raise HttpException(400, 'Some error occurred')
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        data = DoctorSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            doctor = Doctor.objects.get(id=pk)
            # In case it's not Admin -> fails
            if request.ROLE_ID != 1:
                raise HttpException(401, 'You don\t have permission to access this Doctor Information')

            data = DoctorSerializer(doctor, many=False).data

        except Doctor.DoesNotExist:
            return HTTP.response(404, 'Doctor with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        #Allow only Admin to create
        if request.ROLE_ID != 1:
            raise HttpException(400, 'Not Allowed')

        if 'username' not in request.data or 'password' not in request.data or 'email' not in request.data:
            raise HttpException(400, 'Need more data')

        try:
            doctor = Doctor
            doctor.department = request.data['department']
            doctor.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(405, str(e))

        # Send Response
        return HTTP.response(201, 'New doctor account created')

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')