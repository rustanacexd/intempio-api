from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    roles = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'roles', 'fullname')
        read_only_fields = ('username', 'roles')

    def get_fullname(self, obj):
        return obj.get_full_name()


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
