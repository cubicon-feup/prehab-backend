from rest_framework import serializers

from prehab_app.models.User import User
from prehab_app.serializers.UserType import RoleSerializer


class SimpleUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False, read_only=True)

    def to_representation(self, obj):
        data = super(SimpleUserSerializer, self).to_representation(obj)  # the original data

        data['role_id'] = data['role']['id']
        data['role_name'] = data['role']['title']
        del data['role']

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('role')
        return queryset

    class Meta:
        model = User
        fields = ['id', 'name', 'role']


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False, read_only=True)

    def to_representation(self, obj):
        data = super(UserSerializer, self).to_representation(obj)  # the original data

        data['role_id'] = data['role']['id']
        data['role_name'] = data['role']['title']
        del data['role']

        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('role')
        return queryset

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'is_active', 'role')
