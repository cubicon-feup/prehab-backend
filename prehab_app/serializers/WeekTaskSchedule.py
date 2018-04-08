from rest_framework import serializers

from prehab_app.models.WeekTaskSchedule import WeekTaskSchedule
from prehab_app.serializers.Task import TaskSerializer


class WeekTaskScheduleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    def to_representation(self, obj):
        data = super(WeekTaskScheduleSerializer, self).to_representation(obj)  # the original data

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('task')
        return queryset

    class Meta:
        model = WeekTaskSchedule
        fields = '__all__'
