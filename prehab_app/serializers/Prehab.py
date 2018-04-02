from rest_framework import serializers

from prehab_app.models.Prehab import Prehab


class PrehabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prehab
        fields = '__all__'
