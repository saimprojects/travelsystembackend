from rest_framework import serializers
from .models import Client, ClientNote


class ClientNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = ClientNote
        fields = ['id', 'client', 'note', 'created_by', 'created_by_name', 'created_at']
        # ✅ client ko read_only kar diya so add_note action me client required nahi hoga
        read_only_fields = ['id', 'client', 'created_by', 'created_at']


class ClientSerializer(serializers.ModelSerializer):
    notes = ClientNoteSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = [
            'id', 'agency', 'name', 'phone_number', 'alternative_number',
            'email', 'passport_number', 'cnic', 'address',
            'created_by', 'created_by_name', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'agency', 'created_by', 'created_at', 'updated_at']


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'name', 'phone_number', 'alternative_number',
            'email', 'passport_number', 'cnic', 'address'
        ]
