from rest_framework import serializers

from prehab_app.models.Doctor import Doctor
from prehab_app.serializers.DoctorPatient import DoctorPatientSerializer
from prehab_app.serializers.User import UserSerializer


class FullDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorPatientSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, required=True)

    def to_representation(self, obj):
        data = super(FullDoctorSerializer, self).to_representation(obj)  # the original data
        data['patients'] = data['doctor']
        data = {**data['user'], **data}
        del data['doctor']
        del data['user']
        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('doctor')
        return queryset

    def get_user(self, obj):
        user = UserSerializer(obj.id).data
        obj['name'] = user['name']
        obj['name'] = user['name']
        for doctor in obj:
            doctor['user'] = UserSerializer(doctor['id']).data
        return obj

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=True)

    def to_representation(self, obj):
        data = super(DoctorSerializer, self).to_representation(obj)  # the original data
        data = {**data['user'], **data}
        del data['user']
        return data

    class Meta:
        model = Doctor
        fields = '__all__'


class SimpleDoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=True)

    def to_representation(self, obj):
        data = super(SimpleDoctorSerializer, self).to_representation(obj)  # the original data
        data = {
            'id': data['user']['id'],
            'name': data['user']['name']
        }
        return data

    class Meta:
        model = Doctor
        fields = '__all__'
