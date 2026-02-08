from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Service
from .serializers import (
    ServiceSerializer,
    ServiceCreateSerializer,
    ServiceAgentSerializer,
    ServiceAgentListSerializer
)
from users.permissions import IsAgencyOwnerOrManager, AgencyDataIsolation


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing services.
    Owner and Manager have full access.
    Agents can only view services with limited details.
    """
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated, AgencyDataIsolation]

    def get_serializer_class(self):
        user = self.request.user

        # Agents get limited serializer
        if user.role == 'agent':
            # LIST => limited fields (no include)
            if self.action == 'list':
                return ServiceAgentListSerializer

            # RETRIEVE (detail) => include show for Details button
            if self.action == 'retrieve':
                return ServiceAgentSerializer

            # fallback (shouldn't happen because agent can't create/update)
            return ServiceAgentListSerializer

        if self.action == 'create':
            return ServiceCreateSerializer
        return ServiceSerializer

    def get_permissions(self):
        """
        Owner and Manager can create/update/delete.
        Agents can only list and retrieve.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAgencyOwnerOrManager(), AgencyDataIsolation()]
        return [IsAuthenticated(), AgencyDataIsolation()]

    def get_queryset(self):
        """Filter services by agency"""
        user = self.request.user
        if user.is_superuser or user.role == 'super_user':
            return Service.objects.all()
        return Service.objects.filter(agency=user.agency)

    def perform_create(self, serializer):
        """Automatically set agency when creating service"""
        serializer.save(agency=self.request.user.agency)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a service"""
        service = self.get_object()
        service.status = 'active'
        service.save()
        return Response({'status': 'Service activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a service"""
        service = self.get_object()
        service.status = 'inactive'
        service.save()
        return Response({'status': 'Service deactivated'})
