from rest_framework import serializers

from prehab_app.models.PatientConstraintType import PatientConstraintType
from prehab_app.serializers.ConstraintType import ConstraintTypeNameSerializer


class PatientConstraintTypeSerializer(serializers.ModelSerializer):
    constraint_type = ConstraintTypeNameSerializer(many=False, read_only=True)

    def to_representation(self, obj):
        data = super(PatientConstraintTypeSerializer, self).to_representation(obj)  # the original data
        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('patient_constraints', 'patient')
        return queryset

    class Meta:
        model = PatientConstraintType
        fields = '__all__'
