from rest_framework import serializers

from prehab_app.models.ConstraintType import ConstraintType


class ConstraintTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstraintType
        fields = '__all__'
