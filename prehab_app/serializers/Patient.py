from rest_framework import serializers

from prehab_app.models.Patient import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
