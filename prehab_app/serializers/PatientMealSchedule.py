from rest_framework import serializers

from prehab_app.models.PatientMealSchedule import PatientMealSchedule
from prehab_app.serializers.Meal import MealSerializer


class PatientMealScheduleSerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=False, read_only=True)

    def to_representation(self, obj):
        data = super(PatientMealScheduleSerializer, self).to_representation(obj)  # the original data

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('patient_meal')
        return queryset

    class Meta:
        model = PatientMealSchedule
        fields = ('week_number', 'day_number', 'meal_order', 'meal')


class SimplePatientMealScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientMealSchedule
        fields = '__all__'
