from rest_framework.permissions import IsAuthenticated

from prehab.settings.base import PERMISSIONS
from prehab_app.models.Role import Role


class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        # TODO - Caceteiro por causa do CORS
        return True
        # if request.method == 'OPTIONS':
        #     return True
        # return request.user and request.user.is_authenticated


class Permission:
    @staticmethod
    def verify(request, allowed):
        if not PERMISSIONS:
            return True

        role_title = Role.objects.which_role(request.ROLE_ID)

        return role_title in allowed
