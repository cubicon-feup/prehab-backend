from rest_framework import serializers

from prehab_app.models import ScheduleWeekTask


class ScheduleWeekTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleWeekTask
        fields = '__all__'
