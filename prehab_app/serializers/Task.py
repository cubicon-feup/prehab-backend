from rest_framework import serializers

from prehab_app.models.Task import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class FullTaskSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(FullTaskSerializer, self).to_representation(obj)  # the original data

        data['task_type_id'] = data['task_type']
        data['task_type'] = obj.get_task_type_display()

        return data

    class Meta:
        model = Task
        fields = '__all__'
