from rest_framework import serializers

from app.models import Person, Group


class LoginModelSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=155)
    password = serializers.CharField(max_length=155)

    class Meta:
        model = Person
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class PersonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ()


class PersonModelSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'score']


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ()
