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

            user = User.objects.filter(activation_code=request.data['activation_code']).get()
            if user.is_active:
                raise HttpException(400, 'You are already active.')

            user.password = request.data['password']
            user.is_active = True
            user.save()

        except User.DoesNotExist:
            return HTTP.response(404, 'Invalid Activation Code.')
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, 'User Activated.')
