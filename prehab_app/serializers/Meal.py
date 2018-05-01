from rest_framework import serializers

from prehab_app.models.Meal import Meal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
