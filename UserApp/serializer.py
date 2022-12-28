from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "first_name", "last_name", "groups"]
        depth = 1


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password'
                  )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = CustomUser.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return customer
