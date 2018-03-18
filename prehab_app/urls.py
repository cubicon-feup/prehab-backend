from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from prehab_app.views.Api import ApiViewSet

router = DefaultRouter()

urlpatterns = [

    url(r'api/',
        ApiViewSet.as_view({
            'get': 'test_endpoint',
            # 'post': 'insert',
            # 'put': 'update_multiple',
            # 'delete': 'delete_multiple',
        }),
        name='Testing'),



    url(r'^', include(router.urls)),
]
