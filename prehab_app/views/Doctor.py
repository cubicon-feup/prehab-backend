import string
import random

import bcrypt
from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab_app.models import Role
from prehab_app.models.Doctor import Doctor
from prehab_app.models.User import User
from prehab_app.serializers.Doctor import DoctorSerializer, FullDoctorSerializer


class DoctorViewSet(GenericViewSet):

    def list(self, request):
        try:
            # In case it's a patient -> don't allow it
            if request.ROLE_ID == 3:
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.', 'You don\'t have acces to this resouurce.')

            doctors = self.paginate_queryset(Doctor.objects.all())
            queryset = self.paginate_queryset(doctors)

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado', 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        data = DoctorSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            # In case it's not Admin -> fails
            if request.ROLE_ID != 1 and request.USER_ID != pk:
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.', 'You don\'t have acces to this resouurce.')

            doctor = Doctor.objects.get(user_id=pk)
            data = FullDoctorSerializer(doctor, many=False).data

        except Doctor.DoesNotExist:
            return HTTP.response(404, 'Doctor com id {} não foi encontrado.'.format(str(pk)))
        except ValueError:
            return HTTP.response(404, 'Url com formato inválido.', 'Invalid URL format. {}'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado', 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, data=data)

    @staticmethod
    def create(request):
        try:
            if request.ROLE_ID != 1:
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.', 'You don\'t have acces to this resouurce.')

            # 1. Check schema
            SchemaValidator.validate_obj_structure(request.data, 'doctor/create.json')

            # 2. Add new User
            new_user = User(
                name=request.data['name'] if 'name' in request.data else None,
                username=request.data['username'],
                email=request.data['email'],
                phone=request.data['phone'] if 'phone' in request.data else None,
                password=bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt().encode('utf-8')),
                role=Role.objects.doctor_role().get(),
                activation_code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                is_active=True,
            )
            new_user.save()

            # 3 Create new Doctor
            doctor = Doctor(
                user=new_user,
                department=request.data['department'] if 'department' in request.data else None
            )
            doctor.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado', 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(201, 'Doctor criado com succeso.')

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405)

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405)
