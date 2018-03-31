import jwt

from prehab.settings import JWT_SECRET, JWT_ALGORITHM


class PrehabGlobalMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        jwt_encoded = request.META.get('HTTP_JWT', None)
        jwt_decoded = jwt.decode(jwt_encoded, JWT_SECRET, algorithm=JWT_ALGORITHM)

        request.USER_ID = jwt_decoded['user_id']
        request.ROLE_ID = jwt_decoded['role_id']

        response = self.get_response(request)
        return response
