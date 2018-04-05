from rest_framework.decorators import list_route
from rest_framework.viewsets import GenericViewSet
from prehab.helpers.HttpResponseHandler import HTTP

from prehab.helpers.HttpException import HttpException
from prehab_app.models import User


class UserViewSet(GenericViewSet):
    @staticmethod
    @list_route(methods=['post'])
    def activate(request):
        try:
            if 'activation_code' not in request.data or 'password' not in request.data:
                raise HttpException(400, 'You need to send activation code and password')

            user = User.objects.get(pk=request.USER_ID)
            if user.is_active:
                raise HttpException(400, 'You are already active.')
            if user.activation_code != request.data:
                raise HttpException(400, 'Invalid Activation Code.')

            user.password = request.data['password']
            user.is_active = True
            user.save()

        except User.DoesNotExist:
            return HTTP.response(404, 'Invalid User.')
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)

        return HTTP.response(200, 'User Activated.')
