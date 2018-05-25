import bcrypt
from rest_framework.decorators import list_route
from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab_app.models import User


class UserViewSet(GenericViewSet):
    @staticmethod
    @list_route(methods=['post'])
    def activate(request):
        try:
            # 1.2. Check schema
            SchemaValidator.validate_obj_structure(request.data, 'user/activate.json')

            user = User.objects.filter(activation_code=request.data['activation_code']).get()
            if user.is_active:
                raise HttpException(400, 'O user já está ativo.', 'The user is already active.')

            user.password = bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt().encode('utf-8'))
            user.is_active = True
            user.save()

        except User.DoesNotExist:
            return HTTP.response(404, 'Código de ativação inválido.', 'Activation code invalid.')
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400,
                                 'Ocorreu um erro inesperado',
                                 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, 'Utilizador ativado com sucesso.')
