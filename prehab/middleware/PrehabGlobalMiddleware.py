import jwt
from jwt import DecodeError

from prehab.helpers.HttpResponseHandler import HTTP
from django.conf import settings


class PrehabGlobalMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.path not in ('/api/login/', '/api/login', '/api/user/activate/', '/api/user/activate'):
            if 'HTTP_JWT' not in request.META:
                return HTTP.response(401, 'Token not present')

            try:
                jwt_encoded = request.META['HTTP_JWT']
                jwt_decoded = jwt.decode(jwt_encoded, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
            except DecodeError:
                return HTTP.response(401, 'Token not valid.')

            request.USER_ID = jwt_decoded['user_id']
            request.ROLE_ID = jwt_decoded['role_id']

        return self.get_response(request)
