from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from prehab_app.views.Auth import AuthViewSet
from prehab_app.views.Doctor import DoctorViewSet
from prehab_app.views.FullTaskSchedule import FullTaskScheduleViewSet
from prehab_app.views.Notification import NotificationViewSet
from prehab_app.views.Patient import PatientViewSet
from prehab_app.views.PatientTaskSchedule import PatientTaskScheduleViewSet
from prehab_app.views.Prehab import PrehabViewSet
from prehab_app.views.Task import TaskViewSet
from prehab_app.views.TaskSchedule import TaskScheduleViewSet
from prehab_app.views.User import UserViewSet

router = routers.DefaultRouter()

router.register(r'task', TaskViewSet, 'crud-task')
router.register(r'patient', PatientViewSet, 'crud-patient')
router.register(r'doctor', DoctorViewSet, 'crud-doctor')
router.register(r'user', UserViewSet, 'crud-user')
router.register(r'prehab', PrehabViewSet, 'crud-prehab')
router.register(r'schedule/task/full', FullTaskScheduleViewSet, 'crud-full-task-schedule')
router.register(r'schedule/task', TaskScheduleViewSet, 'crud-task-schedule')
router.register(r'notification', NotificationViewSet, 'crud-task-notification')

urlpatterns = [
    url(r'login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    url(r'logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    url(r'patient/schedule/task/', PatientTaskScheduleViewSet.as_view({'post': 'update'}), name='updateTaskSchedule'),
    path('', include(router.urls))
]
