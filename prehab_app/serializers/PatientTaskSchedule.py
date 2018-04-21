from rest_framework import serializers

from prehab_app.models.PatientTaskSchedule import PatientTaskSchedule
from prehab_app.serializers.Task import TaskSerializer


class PatientTaskScheduleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=False, read_only=True)

    def to_representation(self, obj):
        data = super(PatientTaskScheduleSerializer, self).to_representation(obj)  # the original data

        data['task']['expected_repetitions'] = data['expected_repetitions']
        del data['expected_repetitions']

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('patient_task')
        return queryset

    class Meta:
        model = PatientTaskSchedule
        fields = ('week_number', 'day_number', 'expected_repetitions', 'status', 'task')


class SimplePatientTaskScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientTaskSchedule
        fields = '__all__'
