from django.http import JsonResponse


class HTTP:

    @staticmethod
    def response(http_code, details="", data=None):
        message = ''
        if http_code == 200:
            message = "Success"
        if http_code == 201:
            message = "Created"
        if http_code == 202:
            message = "Accepted"
        if http_code == 204:
            message = "No content"
        if http_code == 400:
            message = "Bad request"
        if http_code == 401:
            message = "Unauthorized"
        if http_code == 403:
            message = "Forbidden"
        if http_code == 404:
            message = "Not found"
        if http_code == 405:
            message = "Method not allowed"
        if http_code == 500:
            message = "Internal error"
        if http_code == 501:
            message = "Not Implemented"

        # GATHER LOGS
        res = {
            "code": http_code,
            "message": message,
            "details": details,
            "data": data
        }

        return JsonResponse(res, status=res['code'])

