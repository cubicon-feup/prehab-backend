from rest_framework import serializers

from prehab_app.models.Patient import Patient
from prehab_app.serializers.PatientConstraintType import PatientConstraintTypeSerializer
from prehab_app.serializers.Prehab import PrehabSerializer


class PatientWithPrehabSerializer(serializers.ModelSerializer):
    prehab_patient = PrehabSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        data = super(PatientWithPrehabSerializer, self).to_representation(obj)  # the original data
        data['prehab'] = [prehab for prehab in data['prehab_patient'] if prehab['status'] < 4]
        data['prehab'] = data['prehab'][0] if len(data['prehab']) > 0 else {}
        del data['prehab_patient']
        return data

    class Meta:
        model = Patient
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientWithConstraintsSerializer(serializers.ModelSerializer):
    patient_constraints = PatientConstraintTypeSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        data = super(PatientWithConstraintsSerializer, self).to_representation(obj)  # the original data
        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('patient_constraints', 'patient')
        return queryset

    class Meta:
        model = Patient
        fields = '__all__'
