from rest_framework import serializers

from prehab_app.models.DoctorPatient import DoctorPatient
from prehab_app.serializers.Patient import PatientWithPrehabSerializer


class DoctorPatientSerializer(serializers.ModelSerializer):
    patient = PatientWithPrehabSerializer(many=False, read_only=True)

    def to_representation(self, obj):
        data = super(DoctorPatientSerializer, self).to_representation(obj)  # the original data
        data = data['patient']
        return data

    class Meta:
        model = DoctorPatient
        fields = '__all__'