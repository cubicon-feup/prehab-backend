# import SchemaValidator

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
            # 0. Validate Input (username and password)
            if 'username' not in request.data or 'password' not in request.data:
                raise HttpException(400, 'You need to send Username and Password.')

            # 1. Check if pair username-password is correct
            user = User.objects.match_credentials(request.data['username'], request.data['password'])
            if len(user) == 0:
                raise HttpException(401, 'Some error occurred with your credentials.')

            # 2. Get Relevant Information of the User
            user = user.get()

            # In Case of a Patient - only if platform is MOBILE
            # In Case of a Doctor - only if platform is WEB
            if (user.role.id == 3 and request.PLATFORM != 'mobile') or (user.role.id == 2 and request.PLATFORM != 'web'):
                raise HttpException(403, 'You are not allowed to access here.')

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

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        data = {
            'jwt': jwt_encoded,
            'role': user.role.title
        }

        if prehab_id is not None:
            data['prehab_id'] = prehab_id

        return HTTP.response(200, '', data)

    @staticmethod
    def logout(request):
        # TODO - Not Implemented - blacklist token
        return HTTP.response(200, '', None)
