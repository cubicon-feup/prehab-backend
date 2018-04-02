from rest_framework import serializers

from prehab_app.models.Doctor import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
