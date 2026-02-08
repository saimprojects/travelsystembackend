from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Agency
from .serializers import AgencySerializer, AgencyUpdateSerializer, AgencyPublicSerializer
from users.permissions import IsAgencyOwnerOrManager

User = get_user_model()


class AgencyPublicView(generics.RetrieveAPIView):
    """
    ✅ PUBLIC: View for any authenticated user to get basic agency info.
    Used by frontend for invoices, display, etc.
    """
    serializer_class = AgencyPublicSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Return the user's agency or default"""
        user = self.request.user
        
        # Try to get user's agency
        if hasattr(user, 'agency') and user.agency:
            return user.agency
        
        # Return a default agency object (won't be saved to DB)
        return Agency(
            id=0,
            name="Your Travel Agency",
            phone_number="+92 300 1234567",
            email="info@travelagency.com",
            address="Karachi, Pakistan",
            status="active"
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Override to ensure we always return data"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            # Fallback response
            return Response({
                'name': 'Your Travel Agency',
                'phone_number': '+92 300 1234567',
                'email': 'info@travelagency.com',
                'address': 'Karachi, Pakistan',
                'status': 'active'
            })


class AgencyDetailView(generics.RetrieveUpdateAPIView):
    """
    ✅ ADMIN: View for agency owners/managers to view and update agency details.
    Only accessible to owners/managers.
    """
    serializer_class = AgencyUpdateSerializer
    permission_classes = [IsAuthenticated, IsAgencyOwnerOrManager]
    
    def get_object(self):
        """Return the user's agency"""
        user = self.request.user
        
        if not hasattr(user, 'agency') or not user.agency:
            # Create a default agency if none exists (for admin users)
            agency, created = Agency.objects.get_or_create(
                name=f"{user.username}'s Agency",
                defaults={
                    'email': user.email,
                    'phone_number': 'N/A',
                    'address': 'N/A',
                    'status': 'active'
                }
            )
            user.agency = agency
            user.save()
        
        return user.agency
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AgencySerializer
        return AgencyUpdateSerializer


class CheckAgencyStatusView(APIView):
    """
    ✅ Check agency status (used during login).
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if not hasattr(user, 'agency') or not user.agency:
            return Response({
                'detail': 'No agency associated with this user account.',
                'status': 'no_agency',
                'has_access': False
            }, status=status.HTTP_200_OK)  # Changed to 200 for frontend handling
        
        agency = user.agency
        agency_status = agency.status.lower() if agency.status else 'inactive'
        
        response_data = {
            'agency_id': agency.id,
            'agency_name': agency.name,
            'agency_status': agency_status,
            'status_display': agency.get_status_display(),
            'has_access': agency_status == 'active'
        }
        
        if agency_status != 'active':
            if agency_status == 'inactive':
                response_data['detail'] = 'Agency account is INACTIVE. Please contact administrator.'
            elif agency_status in ['suspended', 'locked']:
                response_data['detail'] = f'Agency account is {agency_status.upper()}. Account has been restricted.'
            elif agency_status == 'pending':
                response_data['detail'] = 'Agency account is PENDING APPROVAL. Please wait for review.'
            else:
                response_data['detail'] = f'Agency account status: {agency_status.upper()}. Account is not active.'
        
        return Response(response_data, status=status.HTTP_200_OK)