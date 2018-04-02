from rest_framework import serializers

from prehab_app.models.PatientConstraintType import PatientConstraintType


class PatientConstraintTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConstraintType
        fields = '__all__'
