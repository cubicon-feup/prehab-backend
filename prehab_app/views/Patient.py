import string
from datetime import datetime
import random

from rest_framework.viewsets import GenericViewSet

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab.helpers.SchemaValidator import SchemaValidator
from prehab.permissions import Permission
from prehab_app.models import ConstraintType, PatientConstraintType, Doctor, Role, User
from prehab_app.models.DoctorPatient import DoctorPatient
from prehab_app.models.Patient import Patient
from prehab_app.serializers.Patient import PatientSerializer


class PatientViewSet(GenericViewSet):

    def list(self, request):
        try:
            # In case it's an Admin -> Retrieve ALL patients info
            if request.ROLE_ID == 1:
                queryset = self.paginate_queryset(Patient.objects.all())
            # In case it's a Doctor -> Retrieve ALL his/her patients info
            elif request.ROLE_ID == 2:
                patients_ids = list(DoctorPatient.objects.filter(doctor_id=request.USER_ID).values_list('patient_id', flat=True))
                queryset = self.paginate_queryset(Patient.objects.filter(pk__in=patients_ids))
            # In case it's a Patient -> Retrieve info about that specific patient
            elif request.ROLE_ID == 3:
                return PatientViewSet.retrieve(request, request.USER_ID)
            else:
                raise HttpException(400, 'Some error occurred')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

        data = PatientSerializer(queryset, many=True).data

        return HTTP.response(200, '', data=data, paginator=self.paginator)

    @staticmethod
    def retrieve(request, pk=None):
        try:
            patient = Patient.objects.get(pk=pk)

            # In case it's a Doctor -> check if he/she has permission
            if request.ROLE_ID == 2 and DoctorPatient.objects.filter(doctor=request.USER_ID).filter(patient=patient).count == 0:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')
            # In case it's a Patient -> check if it's own information
            elif request.ROLE_ID == 3 and request.USER_ID == patient.id:
                raise HttpException(401, 'You don\t have permission to access this Patient Information')

            data = PatientSerializer(patient, many=False).data

        except Patient.DoesNotExist:
            return HTTP.response(404, 'Patient with id {} does not exist'.format(str(pk)))
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred')

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
