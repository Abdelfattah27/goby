from rest_framework import serializers
from .models import *
from django.conf import settings


class ClientReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="client-detail")
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        exclude = ["password"]

    def get_created_at(self, obj):
        return f"{obj.created_at.astimezone(settings.CAIRO_TZ):%Y-%m-%d - %H:%M:%S}"


class ClientWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "password",
            "confirm_password",
            "phone",
            "is_deliveryman",
            "is_approaved_by_admin",
            "address_current",
            "address_latitude",
            "address_longitude",
            "gender",
            "profile_image",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        confirm_password = validated_data.pop("confirm_password", None)
        if password != confirm_password:
            raise serializers.ValidationError(
                [{"confirm_password": "password doesn't match"}]
            )
        client = Client(**validated_data)
        if password:
            client.set_password(password)

        client.save()

        return client

    def update(self, instance, validated_data):
        validated_data.pop("password", None)
        print(validated_data)
        return super(ClientWriteSerializer, self).update(instance, validated_data)


class ClientPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Client
        fields = ["current_password", "new_password", "confirm_password"]

    def validate_current_password(self, value):
        client = Client.objects.get(id=self.context.get("id"))
        if not client.check_password(value):
            raise serializers.ValidationError("Incorrect password")
        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": ["Password doesn't match"]}
            )
        return attrs
