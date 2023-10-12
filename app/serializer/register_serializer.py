from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from app.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", 'username', "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        password = validate_data.pop("password")
        hashed_password = make_password(password)
        user = User.objects.create(**validate_data,
                                   password=hashed_password)
        return user
