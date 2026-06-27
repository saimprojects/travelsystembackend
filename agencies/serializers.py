from rest_framework import serializers
from .models import Agency


class AgencyPublicSerializer(serializers.ModelSerializer):
    """
    PUBLIC: Basic agency info for invoices and display.
    """
    class Meta:
        model = Agency
        fields = [
            'id',
            'name',
            'phone_number',
            'email',
            'address',
            'status',
            'logo_url',
            'invoice_template',
            'advanced_features_enabled',
        ]
        read_only_fields = ['id', 'status']


class AgencySerializer(serializers.ModelSerializer):
    """
    FULL: Detailed agency info for admin users.
    """
    user_count = serializers.SerializerMethodField()
    booking_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Agency
        fields = [
            'id',
            'name',
            'phone_number',
            'email',
            'address',
            'status',
            'logo_url',
            'description',
            'invoice_template',
            'advanced_features_enabled',
            'user_count',
            'booking_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_count', 'booking_count', 'advanced_features_enabled']
    
    def get_user_count(self, obj):
        return obj.users.count()
    
    def get_booking_count(self, obj):
        return obj.bookings.count()


class AgencyUpdateSerializer(serializers.ModelSerializer):
    """
    UPDATE: Serializer for updating agency details.
    """
    class Meta:
        model = Agency
        fields = [
            'name',
            'phone_number',
            'email',
            'address',
            'logo',
            'description',
            'invoice_template',
        ]