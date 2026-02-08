from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Client, ClientNote
from .serializers import ClientSerializer, ClientCreateSerializer, ClientNoteSerializer
from users.permissions import CanAccessClients, AgencyDataIsolation


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clients.
    Owner, Manager, and Agent can access.
    """
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, CanAccessClients, AgencyDataIsolation]

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        return ClientSerializer

    def get_queryset(self):
        """Filter clients by agency and support search"""
        user = self.request.user
        queryset = Client.objects.filter(agency=user.agency)

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(email__icontains=search) |
                Q(passport_number__icontains=search) |
                Q(cnic__icontains=search)
            )

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Automatically set agency and created_by when creating client"""
        serializer.save(
            agency=self.request.user.agency,
            created_by=self.request.user
        )

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add a note to a client"""
        client = self.get_object()

        note_text = request.data.get('note', '')
        if not str(note_text).strip():
            return Response({'note': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClientNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=client, created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClientNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing client notes.
    """
    queryset = ClientNote.objects.all()
    serializer_class = ClientNoteSerializer
    permission_classes = [IsAuthenticated, CanAccessClients]

    def get_queryset(self):
        """Filter notes by agency"""
        user = self.request.user
        return ClientNote.objects.filter(client__agency=user.agency).order_by('-created_at')

    def perform_create(self, serializer):
        """Automatically set created_by when creating note"""
        serializer.save(created_by=self.request.user)
