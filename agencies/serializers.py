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
            'phone_number',  # ✅ Now exists in model
            'email',         # ✅ Now exists in model
            'address',       # ✅ Now exists in model
            'status',
            'logo_url'       # ✅ Now exists as property
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
            'phone_number',  # ✅ Now exists
            'email',         # ✅ Now exists
            'address',       # ✅ Now exists
            'status',
            'logo_url',      # ✅ Now exists as property
            'description',   # ✅ Now exists
            'user_count',
            'booking_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_count', 'booking_count']
    
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
            'description'
        ]