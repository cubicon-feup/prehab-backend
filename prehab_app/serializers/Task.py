from rest_framework import serializers

from prehab_app.models.Task import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
