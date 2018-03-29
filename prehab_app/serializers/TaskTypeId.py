from rest_framework import serializers

from prehab_app.models import TaskTypeId


class TaskTypeIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTypeId
        fields = '__all__'
