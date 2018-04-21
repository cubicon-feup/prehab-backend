import datetime

from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models import PatientTaskSchedule
from prehab_app.models.PatientTaskScheduleStatus import PatientTaskScheduleStatus
from prehab_app.models.Prehab import Prehab


class PatientTaskScheduleViewSet(GenericViewSet):

    @staticmethod
    def update(request):
        try:
            data = request.data

            # 1. Validations
            # 1.1. Only Patients can create new Prehab Plans
            if not Permission.verify(request, ['Patient']):
                raise HttpException(401)

            # 1.2. Check schema
            SchemaValidator.validate_obj_structure(data, 'patient_task_schedule/update.json')

            # 1.3. Check if prehab is valid
            prehab = Prehab.objects.get(pk=data['prehab_id'])

            # 1.4. Check if patient is prehab's owner
            if prehab.patient.id != request.USER_ID:
                raise HttpException(400, 'You can\'t update this Prehab Plan')

            # 1.5. Check if Patient Task Schedule is valid
            patient_task_schedule = PatientTaskSchedule.objects.get(pk=data['patient_task_schedule_id'])

            # 1.6. Check if Patient Task Schedule is included in the given prehab
            if patient_task_schedule.prehab.id != prehab.id:
                raise HttpException(400, 'Prehab and Patient Task Schedule does not match.')

            # 2. Update This specific Task in PatientTaskSchedule
            # 2.1. Task completed with success
            if data['completed']:
                patient_task_schedule.status = PatientTaskScheduleStatus.objects.get(pk=3)

            # 2.2. Task not completed
            else:
                patient_task_schedule.status = PatientTaskScheduleStatus.objects.get(pk=4)

            patient_task_schedule.finished_date = datetime.datetime.now()
            patient_task_schedule.save()

            # 3. Report Difficulties - TODO

        except PatientTaskSchedule.DoesNotExist as e:
            return HTTP.response(400, 'Prehab with id of {} does not exist.'.format(request.data['prehab_id']))
        except Prehab.DoesNotExist as e:
            return HTTP.response(400, 'Prehab with id of {} does not exist.'.format(request.data['prehab_id']))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        return HTTP.response(201, '')
