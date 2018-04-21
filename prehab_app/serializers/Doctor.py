from rest_framework import serializers

from prehab_app.models import User
from prehab_app.models.Doctor import Doctor
from prehab_app.serializers.DoctorPatient import DoctorPatientSerializer


class DoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorPatientSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        data = super(DoctorSerializer, self).to_representation(obj)  # the original data
        data['role'] = User.objects.get(id=data['id']).role.title
        data['patients'] = data['doctor']
        del data['doctor']
        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('doctor')
        return queryset

    class Meta:
        model = Doctor
        fields = '__all__'
