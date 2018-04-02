from rest_framework import serializers

from prehab_app.models.TaskType import TaskType


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = '__all__'
