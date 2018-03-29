from rest_framework import serializers

from prehab_app.models import PatientType


class PatientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientType
        fields = '__all__'
