from rest_framework import serializers

from prehab_app.models.Role import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
