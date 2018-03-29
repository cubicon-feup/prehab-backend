from rest_framework import serializers

from prehab_app.models import PrehabStatus


class PrehabStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrehabStatus
        fields = '__all__'
