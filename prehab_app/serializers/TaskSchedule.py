from rest_framework import serializers

from prehab_app.models.TaskSchedule import TaskSchedule
from prehab_app.serializers.WeekTaskSchedule import WeekTaskScheduleSerializer


class TaskScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSchedule
        fields = '__all__'


class FullTaskScheduleSerializer(serializers.ModelSerializer):
    week_task_schedule = WeekTaskScheduleSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        data = super(FullTaskScheduleSerializer, self).to_representation(obj)  # the original data

        data['weeks'] = FullTaskScheduleSerializer.format_weeks(data)
        data.pop('week_task_schedule')

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('week_task_schedule')
        return queryset

    class Meta:
        model = TaskSchedule
        fields = '__all__'

    @staticmethod
    def format_weeks(data):
        new_data = {}
        for record in data['week_task_schedule']:
            new_data.setdefault(record['week_number'], []).append({k: v for k, v in record.items() if k != 'week_number'})

        return [{'week_number': k, 'tasks': v} for k, v in new_data.items()]
