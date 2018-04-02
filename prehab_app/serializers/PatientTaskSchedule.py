from rest_framework import serializers

from prehab_app.models.PatientTaskSchedule import PatientTaskSchedule


class PatientTaskScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTaskSchedule
        fields = '__all__'
