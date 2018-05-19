from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from prehab_app.views.Auth import AuthViewSet
from prehab_app.views.CronJobs import CronJobsViewSet
from prehab_app.views.Doctor import DoctorViewSet
from prehab_app.views.FullTaskSchedule import FullTaskScheduleViewSet
from prehab_app.views.Meal import MealViewSet
from prehab_app.views.Patient import PatientViewSet
from prehab_app.views.PatientTaskSchedule import PatientTaskScheduleViewSet
from prehab_app.views.Prehab import PrehabViewSet
from prehab_app.views.Task import TaskViewSet
from prehab_app.views.TaskSchedule import TaskScheduleViewSet
from prehab_app.views.User import UserViewSet

router = routers.DefaultRouter()

router.register(r'patient/schedule/task', PatientTaskScheduleViewSet, 'crud-patient-task-schedule')
router.register(r'task', TaskViewSet, 'crud-task')
router.register(r'patient', PatientViewSet, 'crud-patient')
router.register(r'doctor', DoctorViewSet, 'crud-doctor')
router.register(r'user', UserViewSet, 'crud-user')
router.register(r'prehab', PrehabViewSet, 'crud-prehab')
router.register(r'schedule/task/full', FullTaskScheduleViewSet, 'crud-full-task-schedule')
router.register(r'schedule/task', TaskScheduleViewSet, 'crud-task-schedule')
router.register(r'meal', MealViewSet, 'crud-meal')

urlpatterns = [
    url(r'login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    url(r'logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    url(r'patient/schedule/task/done', PatientTaskScheduleViewSet.as_view({'put': 'mark_as_done'}), name='updateTaskSchedule'),
    url(r'patient/(?P<pk>\d+)/statistics', PatientViewSet.as_view({'get': 'statistics'}), name='getStatistics'),
    url(r'patient/add_second_doctor', PatientViewSet.as_view({'post': 'add_second_doctor'}), name='add_second_doctor'),

    url(r'cron/tasks', CronJobsViewSet.as_view({'post': 'clean_tasks'}), name='clean_tasks'),
    url(r'cron/prehabs', CronJobsViewSet.as_view({'post': 'clean_prehabs'}), name='clean_prehabs'),

    url(r'prehab/cancel/(?P<pk>\d+)/', PrehabViewSet.as_view({'put': 'cancel'}), name='cancel_prehab'),

    path('', include(router.urls)),
]
