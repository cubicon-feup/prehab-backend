from rest_framework.permissions import IsAuthenticated


class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        # TODO - Caceteiro por causa do CORS
        return True
        # if request.method == 'OPTIONS':
        #     return True
        # return request.user and request.user.is_authenticated
