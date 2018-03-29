from rest_framework import serializers

from prehab_app.models import DoctorPatient


class DoctorPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPatient
        fields = '__all__'
