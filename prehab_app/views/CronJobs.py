# import SchemaValidator

import datetime

from rest_framework import viewsets

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models import PatientTaskSchedule, Prehab


class CronJobsViewSet(viewsets.ModelViewSet):

    @staticmethod
    def clean_tasks(request):
        try:
            patient_tasks = PatientTaskSchedule.objects.all()

            for patient_task in patient_tasks:
                prehab_init_date = patient_task.prehab.init_date
                task_date = prehab_init_date + datetime.timedelta(days=7 * (patient_task.week_number - 1)) + datetime.timedelta(
                    days=(patient_task.day_number - 1))
                patient_task.date = task_date
                if task_date < datetime.date.today() and patient_task.status == 1:
                    patient_task.status = PatientTaskSchedule.NOT_COMPLETED
                patient_task.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '')

    @staticmethod
    def clean_prehabs(request):
        try:
            prehabs = Prehab.objects.filter(status__lt=3).all()

            for prehab in prehabs:
                # Automatic start prehab
                if prehab.init_date <= datetime.date.today() and prehab.status == 1:
                    prehab.status = Prehab.ONGOING

                # Achieve Prehabs due 30 days
                elif (prehab.expected_end_date + datetime.timedelta(30)) <= datetime.date.today() and prehab.status < 3:
                    prehab.actual_end_date = datetime.date.today()
                    prehab.status = Prehab.CANCEL

                prehab.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '')
