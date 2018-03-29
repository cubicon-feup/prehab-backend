from django.http import JsonResponse
from rest_framework import viewsets


class AuthView(viewsets.ModelViewSet):

    @staticmethod
    def login(request):
        return JsonResponse({'code': 200, 'message': 'Success', 'data': {'jwt': 'xyz'}})
