import datetime

from django.db import transaction
from rest_framework.viewsets import GenericViewSet

from prehab.helpers.DataHelper import DataHelper
from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models import TaskScheduleStatus, Task, PatientTaskSchedule
from prehab_app.models.Doctor import Doctor
from prehab_app.models.DoctorPatient import DoctorPatient
from prehab_app.models.Patient import Patient
from prehab_app.models.PatientTaskScheduleStatus import PatientTaskScheduleStatus
from prehab_app.models.Prehab import Prehab
from prehab_app.models.PrehabStatus import PrehabStatus
from prehab_app.models.TaskSchedule import TaskSchedule
from prehab_app.serializers.Prehab import PrehabSerializer, FullPrehabSerializer


class PrehabViewSet(GenericViewSet):

    def list(self, request):
        try:
            if 'active' in request.GET and request.GET.get('active'):
                prehabs = Prehab.objects.filter(status__not_in=4)
            else:
                prehabs = Prehab.objects

            # In case it's an Admin -> Retrieve ALL PREHABS info
            if request.ROLE_ID == 1:
                prehabs = prehabs.all()
            # In case it's a Doctor -> Retrieve ALL plans created by him
            elif request.ROLE_ID == 2:
                prehabs = prehabs.filter(created_by=request.USER_ID).all()
            # In case it's a Patient -> Retrieve his plan
            elif request.ROLE_ID == 3:
                prehabs = prehabs.filter(patient_id=request.USER_ID).all()
            else:
                raise HttpException(400, 'Some error occurred')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        queryset = self.paginate_queryset(prehabs)
        data = PrehabSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            prehab = Prehab.objects.get(id=pk)
            if request.ROLE_ID != 1 and request.USER_ID not in (prehab.created_by.id.id, prehab.patient.id.id):
                raise HttpException(401, 'You don\'t have permissions to see this Prehab Plan')

        except Prehab.DoesNotExist:
            return HTTP.response(404, 'Prehab with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        data = FullPrehabSerializer(prehab, many=False).data
        return HTTP.response(200, '', data)

    @staticmethod
    def create(request):
        try:
            data = request.data

            # 1. Validations
            # 1.1. Only Doctors can create new Prehab Plans
            if not Permission.verify(request, ['Doctor']):
                raise HttpException(401)

            # 1.2. Check schema
            SchemaValidator.validate_obj_structure(data, 'prehab/create.json')

            # 1.3. Check if patient_id is one of this doctor patients
            patient_id = data['patient_id']
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=request.USER_ID)
            if not DoctorPatient.objects.is_a_match(request.USER_ID, patient_id):
                raise HttpException(400, 'Patient {} is not from Doctor {}.'.format(patient_id, request.USER_ID))

            # 1.4. Check if surgery date is greater than init_date
            surgery_date = datetime.datetime.strptime(data['surgery_date'], "%d-%m-%Y")
            init_date = datetime.datetime.strptime(data['init_date'], "%d-%m-%Y")
            if data['surgery_date'] < data['init_date']:
                raise HttpException(400, 'Surgery Date must be after prehab init.')

            # 1.5. Check if Task Schedule Id was created by this specific doctor or a community Task Schedule (created by an admin
            task_schedule = TaskSchedule.objects.get(id=data['task_schedule_id'])
            if not task_schedule.doctor_can_use(doctor.id.id):
                raise HttpException(400, 'You are not the owner of this task schedule')

            # 2. Transform General Task Schedule to a Custom Patient Task Schedule
            expected_end_date = init_date + datetime.timedelta(days=7 * task_schedule.number_of_weeks)

            # 3. Insert new Prehab
            with transaction.atomic():
                prehab = Prehab(
                    patient=patient,
                    init_date=init_date,
                    expected_end_date=expected_end_date,
                    actual_end_date=None,
                    surgery_date=surgery_date,
                    number_of_weeks=task_schedule.number_of_weeks,
                    status=PrehabStatus.objects.pending(),
                    created_by=doctor
                )
                prehab.save()

                # 4. Insert Patient Tas Schedule
                patient_task_schedule_work_load = DataHelper.patient_task_schedule_work_load(task_schedule)
                for row in patient_task_schedule_work_load:
                    patient_task_schedule = PatientTaskSchedule(
                        prehab=prehab,
                        week_number=row['week_number'],
                        day_number=row['day_number'],
                        task=row['task'],
                        expected_repetitions=1,  # row['repetitions'],
                        actual_repetitions=None,
                        status=PatientTaskScheduleStatus.objects.pending()
                    )
                    patient_task_schedule.save()

            # 4. Add new Notification to Patient (???????????) - TODO

        except Patient.DoesNotExist as e:
            return HTTP.response(400, 'Patient with id of {} does not exist.'.format(request.data['patient_id']))
        except TaskSchedule.DoesNotExist as e:
            return HTTP.response(400, 'Task Schedule with id of {} does not exist.'.format(request.data['task_schedule_id']))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        data = {
            'prehab_id': prehab.id
        }
        return HTTP.response(201, '', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')
