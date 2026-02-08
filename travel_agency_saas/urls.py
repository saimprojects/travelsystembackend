"""
URL configuration for travel_agency_saas project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import LoginView, UserProfileView, UserViewSet
from agencies.views import AgencyPublicView, AgencyDetailView, CheckAgencyStatusView
from services.views import ServiceViewSet
from clients.views import ClientViewSet, ClientNoteViewSet
from bookings.views import (
    BookingViewSet, OnboardViewSet, AnalyticsView, BookingNoteViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'client-notes', ClientNoteViewSet, basename='client-note')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'booking-notes', BookingNoteViewSet, basename='booking-note')
router.register(r'onboard', OnboardViewSet, basename='onboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ AUTHENTICATION ENDPOINTS
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # ✅ AGENCY ENDPOINTS
    path('api/agency/', AgencyDetailView.as_view(), name='agency-detail'),  # Admin only
    path('api/agency/public/', AgencyPublicView.as_view(), name='agency-public'),  # All authenticated users
    path('api/agency/check-status/', CheckAgencyStatusView.as_view(), name='check-agency-status'),
    
    # ✅ ANALYTICS ENDPOINT
    path('api/analytics/', AnalyticsView.as_view(), name='analytics'),
    
    # ✅ ROUTER URLS
    path('api/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)