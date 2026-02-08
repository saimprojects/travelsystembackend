from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    service_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'agency',
            'service_name', 'service_include',
            'service_base_cost', 'service_profit', 'service_total_price',
            'service_duration', 'destination',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'agency', 'created_at', 'updated_at']

    def get_service_total_price(self, obj):
        # property returns Decimal; serializer wants json-safe
        return str(obj.service_total_price)


class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'service_name', 'service_include',
            'service_base_cost', 'service_profit',
            'service_duration', 'destination', 'status'
        ]


class ServiceAgentSerializer(serializers.ModelSerializer):
    """
    Agent serializer:
    - In LIST: limited fields (NO service_include)
    - In RETRIEVE (detail): include service_include (Details button)
    This behavior is controlled from ViewSet (get_serializer_class).
    """
    service_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        # By default agent serializer includes service_include too,
        # but viewset will decide when to use which serializer.
        fields = [
            'id',
            'service_name', 'service_include',
            'service_base_cost', 'service_profit', 'service_total_price',
            'service_duration', 'destination', 'status'
        ]

    def get_service_total_price(self, obj):
        return str(obj.service_total_price)


class ServiceAgentListSerializer(serializers.ModelSerializer):
    """
    Agent LIST serializer (NO service_include)
    """
    service_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id',
            'service_name',
            'service_base_cost', 'service_profit', 'service_total_price',
            'service_duration', 'destination', 'status'
        ]

    def get_service_total_price(self, obj):
        return str(obj.service_total_price)
