import datetime

from django.db import transaction
from rest_framework.viewsets import GenericViewSet

from prehab.helpers.DataHelper import DataHelper
from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models.Doctor import Doctor
from prehab_app.models.DoctorPatient import DoctorPatient
from prehab_app.models.Patient import Patient
from prehab_app.models.PatientConstraintType import PatientConstraintType
from prehab_app.models.PatientMealSchedule import PatientMealSchedule
from prehab_app.models.PatientTaskSchedule import PatientTaskSchedule
from prehab_app.models.Prehab import Prehab
from prehab_app.models.TaskSchedule import TaskSchedule
from prehab_app.serializers.Doctor import SimpleDoctorSerializer
from prehab_app.serializers.Patient import PatientWithConstraintsSerializer
from prehab_app.serializers.Prehab import PrehabSerializer, FullPrehabSerializer


class PrehabViewSet(GenericViewSet):

    def list(self, request):
        try:
            if 'active' in request.GET and request.GET.get('active'):
                prehabs = Prehab.objects.filter(status__not_in=4)
            else:
                prehabs = Prehab.objects.filter(status__lt=4)

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
                raise HttpException(400)

            queryset = self.paginate_queryset(prehabs)
            data = PrehabSerializer(queryset, many=True).data
            for record in data:
                # STATISTICS
                prehab = Prehab.objects.get(pk=record['id'])
                patient_tasks = PatientTaskSchedule.objects.filter(prehab=prehab).all()

                past_patient_tasks = [t for t in patient_tasks if
                                      t.week_number <= prehab.get_current_week_num() and t.day_number <= prehab.get_current_day_num()]

                record['info'] = {
                    'patient_id': prehab.patient.pk,
                    'patient_tag': prehab.patient.patient_tag,
                    'prehab_week_number': prehab.number_of_weeks,
                    'prehab_start_date': prehab.init_date,
                    'prehab_expected_end_date': prehab.expected_end_date,
                    'surgery_day': prehab.surgery_date,
                    'days_until_surgery': prehab.get_days_to_prehab_end() if prehab.get_days_to_prehab_end() else None,
                    'total_activities': len(patient_tasks),
                    'total_activities_until_now': len(past_patient_tasks),
                    'activities_done': len(
                        [t for t in past_patient_tasks if t.status == PatientTaskSchedule.COMPLETED]),
                    'activities_with_difficulty': len([t for t in past_patient_tasks if t.was_difficult]),
                    'activities_not_done': len(
                        [t for t in past_patient_tasks if t.status == PatientTaskSchedule.NOT_COMPLETED]),
                    'prehab_status_id': prehab.status,
                    'prehab_status': prehab.get_status_display(),
                    'number_of_alerts_unseen': len([t for t in past_patient_tasks if
                                                (t.status == PatientTaskSchedule.NOT_COMPLETED or t.was_difficult) and not t.seen_by_doctor]),
                    'number_of_alerts': len([t for t in past_patient_tasks if
                                         (t.status == PatientTaskSchedule.NOT_COMPLETED or t.was_difficult)])
                }

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400,
                                 'Ocorreu um erro inesperado',
                                 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '', data=data)  # , paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            prehab = Prehab.objects.get(pk=pk)
            if request.ROLE_ID != 1 and request.USER_ID not in (prehab.created_by.user.id, prehab.patient.user.id):
                raise HttpException(401, 'Você não tem permissões para ver este prehab.',
                                    'You don\'t have permissions to see this Prehab Plan')

            # STATISTICS
            patient_tasks = PatientTaskSchedule.objects.filter(prehab=prehab).all()
            pass_patient_tasks = [t for t in patient_tasks if
                                  t.week_number <= prehab.get_current_week_num() and t.day_number <= prehab.get_current_day_num()]

            prehab_statistics = {
                'total_activities': len(patient_tasks),
                'total_activities_until_now': len(pass_patient_tasks),
                'activities_done': len([t for t in pass_patient_tasks if t.status == PatientTaskSchedule.COMPLETED]),
                'activities_with_difficulty': len([t for t in pass_patient_tasks if t.was_difficult]),
                'activities_not_done': len(
                    [t for t in pass_patient_tasks if t.status == PatientTaskSchedule.NOT_COMPLETED]),
                'prehab_status_id': prehab.status,
                'prehab_status': prehab.get_status_display()
            }

            # DOCTORS
            prehab_doctors = []
            for doctor_patient in DoctorPatient.objects.filter(patient=prehab.patient).all():
                prehab_doctors.append(SimpleDoctorSerializer(doctor_patient.doctor, many=False).data)

        except Prehab.DoesNotExist:
            return HTTP.response(404, 'Prehab não encontrado', 'Prehab with id {} does not exist'.format(str(pk)))
        except ValueError:
            return HTTP.response(404, 'Url com formato inválido.', 'Invalid URL format. {}'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Ocorreu um erro inesperado',
                                 'Unexpected Error. {}. {}.'.format(type(e).__name__, str(e)))

        data = FullPrehabSerializer(prehab, many=False).data

        data['alerts'] = [
            {
                'patient_task_schedule_id': t['id'],
                'task_title': t['title'],
                'task_description': t['description'],
                'task_type': t['task_type'],
                'status': t['status'],
                'date': t['patient_task_info']['date'],
                'seen_by_doctor': t['patient_task_info']['seen_by_doctor'],
                'doctor_notes': t['patient_task_info']['doctor_notes'],
                'was_difficult': t['patient_task_info']['was_difficult'],
            }
            for d, tasks in data['task_schedule'].items()
            for t in tasks if t['patient_task_info']['was_difficult'] or t['status_id'] == PatientTaskSchedule.NOT_COMPLETED
        ]

        data['number_of_alerts_unseen'] = len([a for a in data['alerts'] if not a['seen_by_doctor']])
        data['number_of_alerts'] = len(data['alerts'])

        data['statistics'] = prehab_statistics
        data['patient'] = PatientWithConstraintsSerializer(prehab.patient, many=False).data
        data['doctors'] = prehab_doctors

        return HTTP.response(200, data=data)

    @staticmethod
    def create(request):
        try:
            data = request.data

            # 1. Validations
            # 1.1. Only Doctors can create new Prehab Plans
            if not Permission.verify(request, ['Admin', 'Doctor']):
                raise HttpException(401,
                                    'Não tem permissões para aceder a este recurso.',
                                    'You don\'t have acces to this resouurce.')

            # 1.2. Check schema
            SchemaValidator.validate_obj_structure(data, 'prehab/create.json')

            # 1.3. Check if patient_id is one of this doctor patients
            patient_id = data['patient_id']
            patient = Patient.objects.get(pk=patient_id)
            doctor = Doctor.objects.get(pk=request.USER_ID)
            if request.ROLE_ID == 2 and not DoctorPatient.objects.is_a_match(request.USER_ID, patient_id):
                raise HttpException(400,
                                    'Paciente não é do médico especificado.',
                                    'Patient {} is not from Doctor {}.'.format(patient_id, request.USER_ID))

            # 1.4. Check if surgery date is greater than init_date
            surgery_date = datetime.datetime.strptime(data['surgery_date'], "%d-%m-%Y")
            init_date = datetime.datetime.strptime(data['init_date'], "%d-%m-%Y")
            if surgery_date < init_date:
                raise HttpException(400,
                                    'Data de cirurgia deve ser posterior à data de inicio de prehab,',
                                    'Surgery Date must be after prehab init.')

            # 1.5. Check if Task Schedule Id was created by
            # this specific doctor or a community Task Schedule (created by an admin)
            task_schedule = TaskSchedule.objects.get(pk=data['task_schedule_id'])
            if request.ROLE_ID != 1 and not task_schedule.doctor_can_use(doctor.user.id):
                raise HttpException(400,
                                    'Você não é o dono deste prehab',
                                    'You are not the owner of this task schedule.')

            # 1.6. Check if this patient has some prehab already
            if Prehab.objects.filter(patient=patient).filter(status__lt=4).count() > 0:
                raise HttpException(400,
                                    'Este paciente já tem um prehab',
                                    'This patient has a prehab already.')

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
                    status=Prehab.PENDING,
                    created_by=doctor
                )
                prehab.save()

                # 4. Insert Patient Task Schedule
                patient_task_schedule_work_load = DataHelper.patient_task_schedule_work_load(task_schedule)
                patient_tasks = []
                for row in patient_task_schedule_work_load:
                    patient_tasks.append(PatientTaskSchedule(
                        prehab=prehab,
                        week_number=row['week_number'],
                        day_number=row['day_number'],
                        task=row['task'],
                        expected_repetitions=1,  # row['repetitions'],
                        actual_repetitions=None,
                        status=PatientTaskSchedule.PENDING
                    ))
                PatientTaskSchedule.objects.bulk_create(patient_tasks)

                # 5. Insert Patient Meal Schedule
                constraint_types = [pct.constraint_type for pct in
                                    PatientConstraintType.objects.filter(patient=patient).all()]
                patient_meal_schedule = DataHelper.patient_meal_schedule(task_schedule.number_of_weeks,
                                                                         constraint_types)
                patient_meals = []
                for row in patient_meal_schedule:
                    patient_meals.append(PatientMealSchedule(
                        prehab=prehab,
                        week_number=row['week_number'],
                        day_number=row['day_number'],
                        meal_order=row['meal_order'],
                        meal=row['meal']
                    ))

                PatientMealSchedule.objects.bulk_create(patient_meals)

        except Patient.DoesNotExist as e:
            return HTTP.response(400, 'Patient with id of {} does not exist.'.format(request.data['patient_id']))
        except TaskSchedule.DoesNotExist as e:
            return HTTP.response(400,
                                 'Task Schedule with id of {} does not exist.'.format(request.data['task_schedule_id']))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Erro Inesperado', 'Unexpected Error: {}.'.format(str(e)))

        # Send Response
        data = {
            'prehab_id': prehab.id
        }
        return HTTP.response(201, '', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405)

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405)

    @staticmethod
    def cancel(request, pk=None):
        try:
            prehab = Prehab.objects.get(pk=pk)

            if not Permission.verify(request, ['Admin', 'Doctor']):
                raise HttpException(401, 'Não tem permissões para aceder a este recurso.',
                                    'You don\'t have acces to this resouurce.')

            if request.ROLE_ID == 2 and not DoctorPatient.objects.is_a_match(request.USER_ID, prehab.patient.id):
                raise HttpException(400,
                                    'Paciente não é paciente do medico especificado.'.format(prehab.patient.id,
                                                                                             request.USER_ID),
                                    'Patient {} is not from doctor {}.'.format(prehab.patient.id, request.USER_ID)
                                    )

            prehab.actual_end_date = datetime.date.today()
            prehab.status = Prehab.CANCEL
            prehab.save()

        except Patient.DoesNotExist as e:
            return HTTP.response(400, 'Paciente não encontrado.',
                                 'Patient with id {} not found.'.format(request.data['patient_id']))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_custom_message, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Erro Inesperado', 'Unexpected Error: {}.'.format(str(e)))

        # Send Response
        return HTTP.response(200, 'Prehab cancelado com sucesso.')
