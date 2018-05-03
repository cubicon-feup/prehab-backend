import datetime

from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models.PatientTaskSchedule import PatientTaskSchedule
from prehab_app.models.Prehab import Prehab
from prehab_app.serializers.PatientTaskSchedule import SimplePatientTaskScheduleSerializer


class PatientTaskScheduleViewSet(GenericViewSet):

    def list(self, request):
        """
        Query Parameters: patient_id
        :param request:
        :return:
        """
        try:
            if 'patient_id' in request.GET and request.GET.get('patient_id'):
                patient_task_schedule = PatientTaskSchedule.objects.filter(patient=request.GET['patient_id'])
            else:
                patient_task_schedule = PatientTaskSchedule.objects

            # In case it's an Admin -> Retrieve ALL PREHABS info
            if request.ROLE_ID == 1:
                patient_task_schedule = patient_task_schedule.all()
            # In case it's a Doctor -> Retrieve ALL plans created by him
            elif request.ROLE_ID == 2:
                patient_task_schedule = patient_task_schedule.filter(prehab__created_by_id=request.USER_ID).all()
            # In case it's a Patient -> Retrieve his plan
            elif request.ROLE_ID == 3:
                patient_task_schedule = patient_task_schedule.filter(prehab__patient_id=request.USER_ID).all()
            else:
                raise HttpException(400, 'Some error occurred')

            queryset = self.paginate_queryset(patient_task_schedule)
            data = SimplePatientTaskScheduleSerializer(queryset, many=True).data

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            patient_task_schedule = PatientTaskSchedule.objects.get(pk=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and request.USER_ID != patient_task_schedule.prehab.created_by.user.id:
                raise HttpException(401, 'You don\'t have permission to access this')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID != patient_task_schedule.prehab.patient.user.id:
                raise HttpException(401, 'You don\'t have permission to access this')

            data = SimplePatientTaskScheduleSerializer(patient_task_schedule, many=False).data

        except PatientTaskSchedule.DoesNotExist:
            return HTTP.response(404, 'Patient with id {} does not exist'.format(str(pk)))
        except ValueError:
            return HTTP.response(404, 'Invalid url format. {}'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        return HTTP.response(405, '')

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def seen(request):
        try:
            data = request.data

            # 1. Validations
            # 1.1. Only Doctors can mark tas schedule as seen
            if not Permission.verify(request, ['Doctor']):
                raise HttpException(401)

            # 1.2. Check schema
            SchemaValidator.validate_obj_structure(data, 'patient_task_schedule/mark_as_seen.json')

            # 1.3. Check if Patient Task Schedule is valid
            patient_task_schedule = PatientTaskSchedule.objects.get(pk=data['patient_task_schedule_id'])
            if patient_task_schedule.status > 2:
                raise HttpException(400, 'This activity was mark as done already.')

            # 1.4. Check if doctor is prehab's owner
            if request.ROLE_ID != 2 or request.ROLE_ID == 2 and patient_task_schedule.prehab.doctor.user.id != request.USER_ID:
                raise HttpException(400, 'You can\'t update this Prehab Plan')

            # 2. Update This specific Task in PatientTaskSchedule
            patient_task_schedule.seen_by_doctor = data['seen']
            patient_task_schedule.doctor_notes = data['doctor_notes'] if 'doctor_notes' in data else ''
            patient_task_schedule.save()

        except PatientTaskSchedule.DoesNotExist:
            return HTTP.response(404, 'Patient Task with id {} does not exist'.format(str(request.data['patient_task_schedule_id'])))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '')

    @staticmethod
    def mark_as_done(request):
        try:
            data = request.data

            # 1. Validations
            # 1.1. Only Patients can create new Prehab Plans
            if not Permission.verify(request, ['Patient']):
                raise HttpException(401)

            # 1.2. Check schema
            SchemaValidator.validate_obj_structure(data, 'patient_task_schedule/mark_as_done.json')

            # 1.3. Check if Patient Task Schedule is valid
            patient_task_schedule = PatientTaskSchedule.objects.get(pk=data['patient_task_schedule_id'])
            if patient_task_schedule.status > 2:
                raise HttpException(400, 'This activity was mark as done already.')

            # 1.4. Check if patient is prehab's owner
            if patient_task_schedule.prehab.patient.user.id != request.USER_ID:
                raise HttpException(400, 'You can\'t update this Prehab Plan')

            # 2. Update This specific Task in PatientTaskSchedule
            # 2.1. Task completed with success
            if data['completed']:
                patient_task_schedule.status = PatientTaskSchedule.COMPLETED

            # 2.2. Task not completed
            else:
                patient_task_schedule.status = PatientTaskSchedule.NOT_COMPLETED

            patient_task_schedule.finished_date = datetime.datetime.now()
            patient_task_schedule.save()

            # 3. Report Difficulties
            patient_task_schedule.was_difficult = data['difficulties']
            patient_task_schedule.patient_notes = data['notes'] if 'notes' in data else ''

            # Doctor only need to check activities that the patient had difficult
            patient_task_schedule.seen_by_doctor = False if data['difficulties'] else True
            patient_task_schedule.save()

        except PatientTaskSchedule.DoesNotExist as e:
            return HTTP.response(400, 'Patient Task Schedule does not exist.')
        except Prehab.DoesNotExist as e:
            return HTTP.response(400, 'Prehab with id of {} does not exist.'.format(request.data['prehab_id']))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        return HTTP.response(200, 'Updated With Success')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
