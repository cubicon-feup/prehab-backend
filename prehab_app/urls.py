from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from prehab_app.views.Auth import AuthViewSet
from prehab_app.views.Task import TaskViewSet

router = routers.DefaultRouter()

router.register(r'task', TaskViewSet, 'crud-task')
router.register(r'schedule/task', TaskViewSet, 'crud-task-schedule')

urlpatterns = [
    url(r'login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    url(r'logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    url(r'web/register_patient/', AuthViewSet.as_view({'post': 'register_patient'}),
        name='register_new_patient'),

    path('', include(router.urls))
]

# from django.conf.urls import url, include
# from rest_framework.routers import DefaultRouter

# from prehab_app.views.Api import ApiViewSet
# router = DefaultRouter()

# urlpatterns = [

#    url(r'api/',
#        ApiViewSet.as_view({
# 'get': 'test_endpoint',
# 'post': 'insert',
# 'put': 'update_multiple',
# 'delete': 'delete_multiple',
#        }),
#        name='Testing'),

#    url(r'^', include(router.urls)),
# ]
