from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from prehab_app.views.Auth import AuthViewSet
from prehab_app.views.Patient import PatientViewSet
from prehab_app.views.Task import TaskViewSet
from prehab_app.views.TaskSchedule import TaskScheduleViewSet
from prehab_app.views.FullTaskSchedule import FullTaskScheduleViewSet
from prehab_app.views.User import UserViewSet

router = routers.DefaultRouter()

router.register(r'task', TaskViewSet, 'crud-task')
router.register(r'patient', PatientViewSet, 'crud-patient')
router.register(r'user', UserViewSet, 'crud-user')
router.register(r'schedule/task/full', FullTaskScheduleViewSet, 'crud-full-task-schedule')
router.register(r'schedule/task', TaskScheduleViewSet, 'crud-task-schedule')

urlpatterns = [
    url(r'login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    url(r'logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),

    url(r'register_patient/',
        AuthViewSet.as_view({'post': "register_patient"}),
        name="register_new_patient"),

    # url(r'schedule/task/full/(?P<task_schedule_id>.+)',
    #     TaskScheduleFullViewSet.as_view({'get': 'get_task_schedule_full'}),
    #     name='get_task_schedule_full'),
    # url(r'schedule/task/full/',
    #     TaskScheduleFullViewSet.as_view({'post': 'create_task_schedule_full'}),
    #     name='create_task_schedule_full'),

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
