from rest_framework import serializers

from prehab_app.models.PatientTaskInfo import PatientTaskInfo


class PatientTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTaskInfo
        fields = '__all__'
