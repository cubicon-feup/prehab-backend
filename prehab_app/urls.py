from django.conf.urls import url
from django.urls import path, include
from prehab_app.views.Auth import AuthView
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    url(r'login/', AuthView.as_view({'post': 'login'}), name='Login in the platform'),
    url(r'web/register_patient/', AuthView.as_view({'post': 'register_patient'}), name='Register a new patient in the platform'),

    path('', include(router.urls))
]


#from django.conf.urls import url, include
#from rest_framework.routers import DefaultRouter

#from prehab_app.views.Api import ApiViewSet
#router = DefaultRouter()

#urlpatterns = [

#    url(r'api/',
#        ApiViewSet.as_view({
            #'get': 'test_endpoint',
            # 'post': 'insert',
            # 'put': 'update_multiple',
            # 'delete': 'delete_multiple',
#        }),
#        name='Testing'),

#    url(r'^', include(router.urls)),
#]
