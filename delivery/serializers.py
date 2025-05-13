# tracking/serializers.py

from rest_framework import serializers
from .models import Credits, Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class CreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credits
        fields = ["amount", "updated_at", "created_at"]
        read_only_fields = ["owner", "updated_at", "created_at"]
