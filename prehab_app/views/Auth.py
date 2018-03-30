import jwt
from django.http import JsonResponse
from rest_framework import viewsets

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.settings import JWT_SECRET, JWT_ALGORITHM
from prehab_app.models import User


class AuthView(viewsets.ModelViewSet):

    @staticmethod
    def login(request):
        try:
            # 0. Validate Input (username and password)
            if 'username' not in request.data or 'password' not in request.data:
                raise HttpException(400, 'You need to send Username and Password.')

            # 1. Check if pair username-password is correct
            login_match = User.objects.match_credentials(request.data['username'], request.data['password'])
            if len(login_match) == 0:
                raise HttpException(401, 'Some error occurred with your credentials.')

            # 2. Get Relevant Information of the User
            user = login_match.get()

            # 3. Get Context Information - TODO

            # 4. Generate JWT
            jwt_data = {
                'user_id': user.id,
                'role_id': user.role.id,
            }
            jwt_encoded = jwt.encode(jwt_data, JWT_SECRET, algorithm=JWT_ALGORITHM).decode('utf-8')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        data = {
            'jwt': jwt_encoded,
            'role': user.role.title
        }
        return HTTP.response(200, '', data)
