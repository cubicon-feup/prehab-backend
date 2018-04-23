from rest_framework import serializers
import datetime

from prehab_app.models import TaskSchedule
from prehab_app.models.Prehab import Prehab
from prehab_app.serializers.PatientTaskSchedule import PatientTaskScheduleSerializer
from prehab_app.serializers.Task import TaskSerializer


class PrehabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prehab
        fields = '__all__'


class FullPrehabSerializer(serializers.ModelSerializer):
    patient_task_schedule = PatientTaskScheduleSerializer(many=True, read_only=True)
    task_schedule = serializers.SerializerMethodField()

    def to_representation(self, obj):
        data = super(FullPrehabSerializer, self).to_representation(obj)  # the original data

        # data['task']['expected_repetitions'] = data['expected_repetitions']
        del data['patient_task_schedule']

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('patient_task_schedule', 'patient_task_schedule__task')
        return queryset

    class Meta:
        model = Prehab
        fields = '__all__'

    @staticmethod
    def get_task_schedule(obj):
        task_schedule = {}
        for task in obj.patient_task_schedule.all():
            date = str(obj.init_date + datetime.timedelta(days=7*(task.week_number - 1)) + datetime.timedelta(days=(task.day_number - 1)))

            if date not in task_schedule:
                task_schedule[date] = []

            task_info = TaskSerializer(task.task, many=False).data
            task_info['id'] = task.id
            task_info['status'] = task.get_status_name()
            task_schedule[date].append(task_info)

        return task_schedule
