from rest_framework import permissions


class IsAgencyOwnerOrManager(permissions.BasePermission):
    """
    Permission for Agency Owner and Manager roles.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['agency_owner', 'manager']
        )


class IsAgencyOwner(permissions.BasePermission):
    """
    Permission for Agency Owner role only.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'agency_owner'
        )


class IsAgent(permissions.BasePermission):
    """
    Permission for Agent role.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'agent'
        )


class IsAccountant(permissions.BasePermission):
    """
    Permission for Accountant role.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'accountant'
        )


class CanAccessClients(permissions.BasePermission):
    """
    Permission for roles that can access clients: Owner, Manager, Agent.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['agency_owner', 'manager', 'agent']
        )


class CanAccessBookings(permissions.BasePermission):
    """
    Permission for roles that can access bookings: Owner, Manager, Agent.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['agency_owner', 'manager', 'agent']
        )


class CanAccessAnalytics(permissions.BasePermission):
    """
    Permission for roles that can access analytics:
    Owner, Manager, Accountant, Agent.

    NOTE:
    Agent ko analytics endpoint access milay ga, lekin agent-specific data filtering
    AnalyticsView ke andar hona chahiye (e.g. bookings = bookings.filter(created_by=user)).
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['agency_owner', 'manager', 'accountant', 'agent']
        )


class AgencyDataIsolation(permissions.BasePermission):
    """
    Ensure users can only access data from their own agency.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and bool(request.user.agency)

    def has_object_permission(self, request, view, obj):
        # Super users can access everything
        if request.user.is_superuser or request.user.role == 'super_user':
            return True

        # Check if object has agency attribute
        if hasattr(obj, 'agency'):
            return obj.agency == request.user.agency

        return False
