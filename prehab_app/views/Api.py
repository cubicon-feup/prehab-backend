from django.http import JsonResponse

# Create your views here.
from rest_framework.viewsets import ModelViewSet


class ApiViewSet(ModelViewSet):

    @staticmethod
    def test_endpoint(request):

        response = {
            'code': 200,
            'message': 'Success. Cubicon rules!',
        }

        return JsonResponse(response, status=200)