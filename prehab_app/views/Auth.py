# import SchemaValidator
import bcrypt
import jwt
from django.conf import settings
from rest_framework import viewsets

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models import Prehab
from prehab_app.models.User import User


class AuthViewSet(viewsets.ModelViewSet):

    @staticmethod
    def login(request):
        try:
            # 1. Check if pair username-password is correct
            user = User.objects.filter(username=request.data['username']).get()
            if not bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password.encode('utf-8')):
                raise HttpException(401, 'Credenciais não válidas.', 'Wrong credentials.')

            # In Case of a Patient - only if platform is MOBILE
            # In Case of a Doctor - only if platform is WEB
            if (user.role.id == 3 and request.PLATFORM != 'mobile') or (user.role.id == 2 and request.PLATFORM != 'web'):
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.', 'You don\'t have acces to this resouurce.')

            # 3. Get Context Information - TODO
            prehab_id = None
            if user.role.id == 3:
                prehab = Prehab.objects.filter(patient_id=user.id)
                if prehab.count():
                    prehab_id = prehab.first().id

            # 4. Generate JWT
            jwt_data = {
                'user_id': user.id,
                'role_id': user.role.id,
            }
            jwt_encoded = jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM).decode('utf-8')

        except User.DoesNotExist as e:
            return HTTP.response(401, 'Utilizador não existe.', 'User not valid.')
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado', 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        # Send Response
        data = {
            'jwt': jwt_encoded,
            'role': user.role.title
        }

        if prehab_id is not None:
            data['prehab_id'] = prehab_id

        return HTTP.response(200, data=data)

    @staticmethod
    def logout(request):
        # TODO - Not Implemented - blacklist token
        return HTTP.response(200)
