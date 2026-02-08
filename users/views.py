from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    PasswordChangeSerializer, EmailTokenObtainPairSerializer
)
from .permissions import IsAgencyOwnerOrManager, AgencyDataIsolation


class LoginView(TokenObtainPairView):
    """
    Custom login view for JWT authentication (email + password).
    Now includes agency status check.
    """
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer  # ✅ NEW
    
    def post(self, request, *args, **kwargs):
        try:
            # First, try to authenticate user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            
            # Check if user has an agency
            if not hasattr(user, 'agency'):
                return Response({
                    'detail': 'No agency associated with this user account.',
                    'status': 'no_agency'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get agency and check status
            agency = user.agency
            agency_status = agency.status.lower() if agency.status else 'inactive'
            
            # Check agency status - only allow login if agency is active
            if agency_status != 'active':
                status_display = agency.get_status_display() if hasattr(agency, 'get_status_display') else agency_status.upper()
                
                # Different messages for different statuses
                if agency_status == 'inactive':
                    message = f'Your agency account is INACTIVE. Please contact administrator.'
                elif agency_status == 'suspended':
                    message = f'Your agency account is SUSPENDED. Account has been restricted due to policy violations.'
                elif agency_status == 'locked':
                    message = f'Your agency account is LOCKED. Account has been locked for security reasons.'
                elif agency_status == 'pending':
                    message = f'Your agency account is PENDING APPROVAL. Please wait for administrator review.'
                else:
                    message = f'Agency account status: {status_display}. Account is not active.'
                
                return Response({
                    'detail': message,
                    'agency_status': agency_status,
                    'agency_name': agency.name,
                    'agency_id': agency.id,
                    'status_display': status_display
                }, status=status.HTTP_403_FORBIDDEN)
            
            # If agency is active, proceed with token generation
            response = super().post(request, *args, **kwargs)
            return response
            
        except AuthenticationFailed as e:
            # Handle authentication failures
            return Response({
                'detail': str(e.detail) if hasattr(e, 'detail') else 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle any other exceptions
            return Response({
                'detail': 'An error occurred during login. Please try again.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for user to get and update their own profile.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing staff users (Owner and Manager can manage).
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAgencyOwnerOrManager, AgencyDataIsolation]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        """Filter users by agency"""
        user = self.request.user
        if user.is_superuser or user.role == 'super_user':
            return User.objects.all()
        return User.objects.filter(agency=user.agency).exclude(role='super_user')

    def perform_create(self, serializer):
        """Automatically set agency when creating user"""
        serializer.save(agency=self.request.user.agency)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a user"""
        user = self.get_object()

        # Prevent deactivating agency owner
        if user.role == 'agency_owner':
            return Response(
                {'error': 'Cannot deactivate agency owner'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = False
        user.save()
        return Response({'status': 'User deactivated'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a user"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'User activated'})

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'status': 'Password changed successfully'})
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)