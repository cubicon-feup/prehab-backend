from rest_framework import serializers

from prehab_app.models.TaskSchedule import TaskSchedule


class TaskScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSchedule
        fields = '__all__'
