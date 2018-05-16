import math
import random
import string
from datetime import datetime

from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models import ConstraintType, PatientConstraintType, Doctor, Role, User, Prehab, PatientTaskSchedule
from prehab_app.models.DoctorPatient import DoctorPatient
from prehab_app.models.Patient import Patient
from prehab_app.serializers.ConstraintType import ConstraintTypeSerializer
from prehab_app.serializers.Doctor import DoctorSerializer
from prehab_app.serializers.Patient import PatientSerializer


class PatientViewSet(GenericViewSet):

    def list(self, request):
        try:
            # In case it's an Admin -> Retrieve ALL patients info
            if request.ROLE_ID == 1:
                queryset = self.paginate_queryset(Patient.objects.all())
            # In case it's a Doctor -> Retrieve ALL his/her patients info
            elif request.ROLE_ID == 2:
                patients_ids = list(
                    DoctorPatient.objects.filter(doctor_id=request.USER_ID).values_list('patient_id', flat=True))
                queryset = self.paginate_queryset(Patient.objects.filter(pk__in=patients_ids))
            # In case it's a Patient -> Retrieve info about that specific patient
            elif request.ROLE_ID == 3:
                return PatientViewSet.retrieve(request, request.USER_ID)
            else:
                raise HttpException(400, 'Some error occurred')

            patients = PatientSerializer(queryset, many=True).data
            data = []
            for patient in patients:
                record = dict(patient)

                # STATISTICS
                prehab = Prehab.objects.filter(patient=patient['user']).first()
                patient_tasks = PatientTaskSchedule.objects.filter(prehab=prehab).all()

                if prehab is None:
                    record['info'] = None
                else:
                    days_to_surgery = (datetime.now().date() - prehab.surgery_date).days
                    current_week_num = math.floor(days_to_surgery / 7)
                    current_day_num = days_to_surgery - 7 * current_week_num
                    pass_patient_tasks = [t for t in patient_tasks if t.week_number <= current_week_num and t.day_number <= current_day_num]

                    record['info'] = {
                        'patient_id': patient['user'],
                        'prehab_week_number': prehab.number_of_weeks,
                        'prehab_start_date': prehab.init_date,
                        'prehab_expected_end_date': prehab.expected_end_date,
                        'surgery_day': prehab.surgery_date,
                        'days_until_surgery': days_to_surgery if days_to_surgery > 0 else None,
                        'total_activities': len(patient_tasks),
                        'total_activities_until_now': len(pass_patient_tasks),
                        'activities_done': len([t for t in pass_patient_tasks if t.status == PatientTaskSchedule.COMPLETED]),
                        'activities_with_difficulty': len([t for t in pass_patient_tasks if t.was_difficult]),
                        'activities_not_done': len([t for t in pass_patient_tasks if t.status == PatientTaskSchedule.NOT_COMPLETED]),
                        'prehab_status_id': prehab.status,
                        'prehab_status': prehab.get_status_display()
                    }

                # DOCTORS
                doctors = DoctorPatient.objects.filter(patient=patient['user']).all()
                record['doctors_associated'] = [DoctorSerializer(d.doctor, many=False).data for d in doctors]

                # CONSTRAINTS
                constraints = PatientConstraintType.objects.filter(patient=patient['user']).all()
                record['constraints'] = [ConstraintTypeSerializer(c.constraint_type, many=False).data for c in constraints]

                data.append(record)

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            patient = Patient.objects.get(pk=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and DoctorPatient.objects.filter(doctor=request.USER_ID).filter(
                    patient=patient).count == 0:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID == patient.id:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')

            data = PatientSerializer(patient, many=False).data

            # STATISTICS
            prehab = Prehab.objects.filter(patient=patient).first()
            if prehab is None:
                data['info'] = None
            else:
                patient_tasks = PatientTaskSchedule.objects.filter(prehab=prehab).all()

                days_to_surgery = (datetime.now().date() - prehab.surgery_date).days
                current_week_num = math.floor(days_to_surgery / 7)
                current_day_num = days_to_surgery - 7 * current_week_num
                pass_patient_tasks = [t for t in patient_tasks if
                                      t.week_number <= current_week_num and t.day_number <= current_day_num]

                data['info'] = {
                    'patient_id': pk,
                    'prehab_week_number': prehab.number_of_weeks,
                    'prehab_start_date': prehab.init_date,
                    'prehab_expected_end_date': prehab.expected_end_date,
                    'surgery_day': prehab.surgery_date,
                    'days_until_surgery': days_to_surgery if days_to_surgery > 0 else None,
                    'total_activities': len(patient_tasks),
                    'total_activities_until_now': len(pass_patient_tasks),
                    'activities_done': len([t for t in pass_patient_tasks if t.status == PatientTaskSchedule.COMPLETED]),
                    'activities_with_difficulty': len([t for t in pass_patient_tasks if t.was_difficult]),
                    'activities_not_done': len([t for t in pass_patient_tasks if t.status == PatientTaskSchedule.NOT_COMPLETED]),
                    'prehab_status_id': prehab.status,
                    'prehab_status': prehab.get_status_display()
                }

            # DOCTORS
            doctors = DoctorPatient.objects.filter(patient=patient.pk).all()
            data['doctors_associated'] = [DoctorSerializer(d.doctor, many=False).data for d in doctors]

            # CONSTRAINTS
            constraints = PatientConstraintType.objects.filter(patient=patient.pk).all()
            data['constraints'] = [ConstraintTypeSerializer(c.constraint_type, many=False).data for c in constraints]

        except Patient.DoesNotExist:
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
        try:
            # 0 - Handle Permissions
            if not Permission.verify(request, ['Doctor']):
                raise HttpException(401)

            data = request.data
            # 1. Check schema
            SchemaValidator.validate_obj_structure(data, 'patient/create.json')

            # 2. Add new User
            new_user = User(
                name='Anónimo',
                username='',
                email=data['email'] if 'email' in data else None,
                phone=data['phone'] if 'phone' in data else None,
                password=None,
                role=Role.objects.patient_role().get(),
                activation_code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                is_active=False,
            )
            new_user.save()
            # 1. Generate Activation Code & Username
            patient_tag = "HSJ{}{}".format(datetime.now().year, str(new_user.id).zfill(4))
            new_user.username = patient_tag
            new_user.save()
            doctor = Doctor.objects.get(pk=request.USER_ID)

            # 3. Add new Patient
            new_patient = Patient(
                user=new_user,
                patient_tag=patient_tag,
                age=data['age'],
                height=data['height'],
                weight=data['weight'],
                sex=data['sex']
            )
            new_patient.save()

            # 4. Create Doctor Patient Association
            relation = DoctorPatient(
                patient=new_patient,
                doctor=doctor
            )

            relation.save()

            # 5. Associate Constraints
            for constraint_id in data['constraints']:
                constraint_type = ConstraintType.objects.get(pk=constraint_id)
                PatientConstraintType(
                    patient=new_patient,
                    constraint_type=constraint_type
                )

            # 6. Generate Task Plan - TODO
            # TODO
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response - access code
        data = {
            'access_code': new_user.activation_code
        }
        return HTTP.response(200, '', data)

    @staticmethod
    def update(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def destroy(request, pk=None):
        return HTTP.response(405, '')

    @staticmethod
    def statistics(request, pk=None):
        try:
            patient = Patient.objects.get(pk=pk)
            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and DoctorPatient.objects.filter(doctor=request.USER_ID).filter(
                    patient=patient).count == 0:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID == patient.id:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')

            prehab = Prehab.objects.filter(patient=patient).first()
            patient_tasks = PatientTaskSchedule.objects.filter(prehab=prehab).all()

            days_to_surgery = (datetime.now().date() - prehab.surgery_date).days
            current_week_num = math.floor(days_to_surgery / 7)
            current_day_num = days_to_surgery - 7 * current_week_num
            pass_patient_tasks = [t for t in patient_tasks if
                                  t.week_number <= current_week_num and t.day_number <= current_day_num]

            data = {
                'patient_id': pk,
                'prehab_week_number': prehab.number_of_weeks,
                'prehab_start_date': prehab.init_date,
                'prehab_expected_end_date': prehab.expected_end_date,
                'surgery_day': prehab.surgery_date,
                'days_until_surgery': days_to_surgery if days_to_surgery > 0 else None,
                'total_activities': len(patient_tasks),
                'total_activities_until_now': len(pass_patient_tasks),
                'activities_done': len([t for t in pass_patient_tasks if t.status == PatientTaskSchedule.COMPLETED]),
                'activities_with_difficulty': len([t for t in pass_patient_tasks if t.was_difficult]),
                'activities_not_done': len(
                    [t for t in pass_patient_tasks if t.status == PatientTaskSchedule.NOT_COMPLETED]),
                'prehab_status_id': prehab.status,
                'prehab_status': prehab.get_status_display()
            }

        except Patient.DoesNotExist:
            return HTTP.response(404, 'Patient with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, '', data)

    @staticmethod
    def add_second_doctor(request):
        try:
            # 0 - Handle Permissions
            if not Permission.verify(request, ['Admin', 'Doctor']):
                raise HttpException(401)

            data = request.data
            # 1. Check schema
            SchemaValidator.validate_obj_structure(data, 'patient/add_second_doctor.json')

            patient = Patient.objects.get(pk=data['patient_id'])
            second_doctor = Doctor.objects.get(pk=data['doctor_id'])
            relation = DoctorPatient.objects.filter(patient=patient)

            # 2. Exceptions:
            # 2.1. If the patient has no doctor and the one calling the api is not an admin
            if relation.count() == 0 and request.ROLE_ID != 1:
                raise Exception('You are not allowed to add doctors to this patient.')
            # 2.2. If patient has 2 doctors already
            if relation.count() > 1:
                raise Exception('One patient can only have 2 doctors associated')
            # 2.3. if the one calling the api is not the first doctor
            if relation.count() == 1 and relation.get().doctor.id != request.USER_ID:
                raise Exception('You are not allowed to add doctors to this patient.')

            # 3. Add new relation
            new_relation = DoctorPatient(
                patient=patient,
                doctor=second_doctor
            )

            new_relation.save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        return HTTP.response(200, '')
