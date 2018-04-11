import random
import string
from datetime import datetime

import jwt
from django.conf import settings
from rest_framework import viewsets

from prehab.helpers.HttpException import HttpException
from prehab.helpers.HttpResponseHandler import HTTP
from prehab_app.models.ConstraintType import ConstraintType
from prehab_app.models.Doctor import Doctor
from prehab_app.models.DoctorPatient import DoctorPatient
from prehab_app.models.Patient import Patient
from prehab_app.models.PatientConstraintType import PatientConstraintType
from prehab_app.models.Role import Role
from prehab_app.models.User import User


class AuthViewSet(viewsets.ModelViewSet):

    @staticmethod
    def login(request):
        try:
            # 0. Validate Input (username and password)
            if 'username' not in request.data or 'password' not in request.data:
                raise HttpException(400, 'You need to send Username and Password.')

            # 1. Check if pair username-password is correct
            login_match = User.objects.match_credentials(request.data['username'], request.data['password'])
            if len(login_match) == 0:
                raise HttpException(401, 'Some error occurred with your credentials.')

            # 2. Get Relevant Information of the User
            user = login_match.get()

            # 3. Get Context Information - TODO

            # 4. Generate JWT
            jwt_data = {
                'user_id': user.id,
                'role_id': user.role.id,
            }
            jwt_encoded = jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM).decode('utf-8')

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        # Send Response
        data = {
            'jwt': jwt_encoded,
            'role': user.role.title
        }
        return HTTP.response(200, '', data)

    @staticmethod
    def logout(request):
        # TODO - Not Implemented - blacklist token
        return HTTP.response(200, '', None)

    @staticmethod
    def register_doctor(request):
        try:
            #1 Check if all needed info was passed
            if 'username' not in request.data or 'password' not in request.data or 'email' not in request.data:
                raise HttpException(400, "Error ")

            # 2. Add new User
            new_user = User(
                name=request.data['name'] if 'name' in request.data else None,
                username=request.data['username'],
                email=request.data['email'],
                phone=request.data['phone'] if 'phone' in request.data else None,
                password=request.data['password'],
                role=Role.objects.doctor_role().get(),
                activation_code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
                is_active=True,
            )
            new_user.save()

            #3 Create new Doctor
            doctor = Doctor(
                id = new_user,
                department=request.data['department'] if 'department' in request.data else None
            )
            doctor.save()


        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, str(e))

        return HTTP.response(200, 'New doctor account created sucessfully')

    @staticmethod
    def register_patient(request):
        try:
            data = request.data
            # 1. Check schema
            # SchemaValidator.validate_obj_structure(data, 'auth/create.json')

            # 0. Validate Input (age, height, weight, sex, constraints, task_schedule_plan_id)
            if 'age' not in request.data or 'height' not in request.data or 'weight' not in request.data or 'sex' not in request.data:
                raise HttpException(400, 'You need to send Age, Height and Weight.')
            if 'constraints' not in request.data and type(request.data['constraints']).__name__ != 'list':
                raise HttpException(400, 'You need to send Constraints.')
            if 'task_schedule_plan_id' not in request.data:
                raise HttpException(400, 'You need to send Task Schedule Id.')

            # 2. Add new User
            new_user = User(
                name='Anónimo',
                username='',
                email=request.data['email'] if 'email' in request.data else None,
                phone=request.data['phone'] if 'phone' in request.data else None,
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
            doctor = Doctor.objects.get(id=request.USER_ID)

            # 3. Add new Patient
            new_patient = Patient(
                id=new_user,
                patient_tag=patient_tag,
                age=request.data['age'],
                height=request.data['height'],
                weight=request.data['weight'],
                sex=request.data['sex']
            )
            new_patient.save()

            # 4. Create Doctor Patient Association
            DoctorPatient(
                patient=new_patient,
                doctor=doctor
            )

            # 5. Associate Constraints
            for constraint_id in request.data['constraints']:
                constraint_type = ConstraintType.objects.get(id=constraint_id)
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
