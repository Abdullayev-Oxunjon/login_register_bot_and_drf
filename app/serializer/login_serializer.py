from django.contrib.auth import authenticate
from rest_framework import serializers

from app.models import User


class LoginModelSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=155)
    password = serializers.CharField(max_length=155)

    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect credentials")

        else:
            raise serializers.ValidationError("Both username and password are required")
        data['user'] = user
        return data
