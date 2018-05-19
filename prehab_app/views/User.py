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
                raise HttpException(400, 'Precisa de enviar código de ativação e nova password.')

            user = User.objects.filter(activation_code=request.data['activation_code']).get()
            if user.is_active:
                raise HttpException(400, 'O user já está ativo.')

            user.password = request.data['password']
            user.is_active = True
            user.save()

        except User.DoesNotExist:
            return HTTP.response(404, 'Código de ativação inválido.')
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, 'Utilizador ativado com sucesso.')
