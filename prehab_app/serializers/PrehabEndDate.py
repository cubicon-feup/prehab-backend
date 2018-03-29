from rest_framework import serializers

from prehab_app.models import PrehabEndDate


class PrehabEndDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrehabEndDate
        fields = '__all__'
