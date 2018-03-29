from rest_framework import serializers

from prehab_app.models import TaskScheduleStatus


class TaskScheduleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskScheduleStatus
        fields = '__all__'
