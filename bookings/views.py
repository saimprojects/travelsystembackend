from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from decimal import Decimal

from .models import Booking, BookingNote
from .serializers import (
    BookingSerializer, BookingCreateSerializer, BookingUpdateSerializer,
    BookingNoteSerializer, BookingAgentSerializer
)
from users.permissions import CanAccessBookings, CanAccessAnalytics, AgencyDataIsolation


# class BookingViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing bookings.
#     Owner, Manager, and Agent can access.
#     """
#     queryset = Booking.objects.all()
#     permission_classes = [IsAuthenticated, CanAccessBookings, AgencyDataIsolation]

#     def get_serializer_class(self):
#         user = self.request.user

#         # Agents get limited serializer
#         if user.role == 'agent':
#             if self.action in ['list', 'retrieve']:
#                 return BookingAgentSerializer

#         if self.action == 'create':
#             return BookingCreateSerializer
#         elif self.action in ['update', 'partial_update']:
#             return BookingUpdateSerializer
#         return BookingSerializer

#     def get_queryset(self):
#         """Filter bookings by agency and support search"""
#         user = self.request.user
#         queryset = Booking.objects.filter(agency=user.agency).select_related(
#             'client', 'service', 'created_by'
#         )

#         # ✅ Agent can only see his own bookings
#         if user.role == 'agent':
#             queryset = queryset.filter(created_by=user)

#         # Search functionality
#         search = self.request.query_params.get('search', None)
#         if search:
#             queryset = queryset.filter(
#                 Q(client__name__icontains=search) |
#                 Q(service__service_name__icontains=search)
#             )

#         # Filter by booking status
#         booking_status = self.request.query_params.get('booking_status', None)
#         if booking_status:
#             queryset = queryset.filter(booking_status=booking_status)

#         # Filter by payment status
#         payment_status = self.request.query_params.get('payment_status', None)
#         if payment_status:
#             queryset = queryset.filter(payment_status=payment_status)

#         # ✅ NEW: Filter missing arrival/departure dates
#         # missing_dates=1 => arrival OR departure missing
#         # missing_dates=0 => both present
#         missing_dates = self.request.query_params.get('missing_dates', None)
#         if missing_dates in ['1', 'true', 'True']:
#             queryset = queryset.filter(
#                 Q(arrival_date__isnull=True) | Q(departure_date__isnull=True)
#             )
#         elif missing_dates in ['0', 'false', 'False']:
#             queryset = queryset.filter(
#                 arrival_date__isnull=False,
#                 departure_date__isnull=False
#             )

#         return queryset.order_by('-created_at')

#     def perform_create(self, serializer):
#         """Automatically set agency and created_by when creating booking"""
#         serializer.save(
#             agency=self.request.user.agency,
#             created_by=self.request.user
#         )

#     @action(detail=True, methods=['post'])
#     def update_payment(self, request, pk=None):
#         """Update payment information for a booking"""
#         booking = self.get_object()
#         paid_amount = request.data.get('paid_amount')
#         payment_method = request.data.get('payment_method')

#         if paid_amount is not None:
#             try:
#                 paid_amount = Decimal(str(paid_amount))
#                 if paid_amount < 0:
#                     return Response(
#                         {'error': 'Paid amount cannot be negative'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#                 booking.paid_amount = paid_amount
#                 if payment_method:
#                     booking.payment_method = payment_method
#                 booking.last_payment_date = timezone.now()
#                 booking.save()

#                 serializer = self.get_serializer(booking)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(
#                     {'error': str(e)},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         return Response(
#             {'error': 'paid_amount is required'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     @action(detail=True, methods=['post'])
#     def add_note(self, request, pk=None):
#         """Add a note to a booking"""
#         booking = self.get_object()
#         serializer = BookingNoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(
#                 booking=booking,
#                 created_by=request.user
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # ✅ NEW: Dates summary endpoint (badge counts)
#     @action(detail=False, methods=['get'])
#     def dates_summary(self, request):
#         """
#         Returns counts for missing arrival/departure dates (for UI badge)
#         """
#         user = request.user
#         qs = Booking.objects.filter(agency=user.agency)

#         # ✅ Agent sees only his own summary
#         if user.role == 'agent':
#             qs = qs.filter(created_by=user)

#         missing_any = qs.filter(Q(arrival_date__isnull=True) | Q(departure_date__isnull=True)).count()
#         missing_arrival = qs.filter(arrival_date__isnull=True).count()
#         missing_departure = qs.filter(departure_date__isnull=True).count()

#         return Response({
#             "missing_any": missing_any,
#             "missing_arrival": missing_arrival,
#             "missing_departure": missing_departure,
#         })




class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    Owner, Manager, and Agent can access.
    """
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, CanAccessBookings, AgencyDataIsolation]

    def get_serializer_class(self):
        user = self.request.user

        # Agents get limited serializer
        if user.role == 'agent':
            if self.action in ['list', 'retrieve']:
                return BookingAgentSerializer

        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        return BookingSerializer

    def get_queryset(self):
        """Filter bookings by agency and support search"""
        user = self.request.user
        queryset = Booking.objects.filter(agency=user.agency).select_related(
            'client', 'service', 'created_by'
        )

        # ✅ Agent can only see his own bookings
        if user.role == 'agent':
            queryset = queryset.filter(created_by=user)

        # ✅ FIXED: Add booking_id filter here
        booking_id = self.request.query_params.get('booking_id', None)
        if booking_id:
            try:
                # Try exact integer match
                booking_id_int = int(booking_id)
                queryset = queryset.filter(id=booking_id_int)
            except ValueError:
                # If not a valid number, return empty
                return Booking.objects.none()

        # Search functionality (general search - name, service)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(client__name__icontains=search) |
                Q(service__service_name__icontains=search)
            )

        # Filter by booking status
        booking_status = self.request.query_params.get('booking_status', None)
        if booking_status:
            queryset = queryset.filter(booking_status=booking_status)

        # Filter by payment status
        payment_status = self.request.query_params.get('payment_status', None)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        # ✅ Filter missing arrival/departure dates
        # missing_dates=1 => arrival OR departure missing
        # missing_dates=0 => both present
        missing_dates = self.request.query_params.get('missing_dates', None)
        if missing_dates in ['1', 'true', 'True']:
            queryset = queryset.filter(
                Q(arrival_date__isnull=True) | Q(departure_date__isnull=True)
            )
        elif missing_dates in ['0', 'false', 'False']:
            queryset = queryset.filter(
                arrival_date__isnull=False,
                departure_date__isnull=False
            )

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Automatically set agency and created_by when creating booking"""
        serializer.save(
            agency=self.request.user.agency,
            created_by=self.request.user
        )

    @action(detail=True, methods=['post'])
    def update_payment(self, request, pk=None):
        """Update payment information for a booking"""
        booking = self.get_object()
        paid_amount = request.data.get('paid_amount')
        payment_method = request.data.get('payment_method')

        if paid_amount is not None:
            try:
                paid_amount = Decimal(str(paid_amount))
                if paid_amount < 0:
                    return Response(
                        {'error': 'Paid amount cannot be negative'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                booking.paid_amount = paid_amount
                if payment_method:
                    booking.payment_method = payment_method
                booking.last_payment_date = timezone.now()
                booking.save()

                serializer = self.get_serializer(booking)
                return Response(serializer.data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {'error': 'paid_amount is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add a note to a booking"""
        booking = self.get_object()
        serializer = BookingNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                booking=booking,
                created_by=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Dates summary endpoint (badge counts)
    @action(detail=False, methods=['get'])
    def dates_summary(self, request):
        """
        Returns counts for missing arrival/departure dates (for UI badge)
        """
        user = request.user
        qs = Booking.objects.filter(agency=user.agency)

        # ✅ Agent sees only his own summary
        if user.role == 'agent':
            qs = qs.filter(created_by=user)

        missing_any = qs.filter(Q(arrival_date__isnull=True) | Q(departure_date__isnull=True)).count()
        missing_arrival = qs.filter(arrival_date__isnull=True).count()
        missing_departure = qs.filter(departure_date__isnull=True).count()

        return Response({
            "missing_any": missing_any,
            "missing_arrival": missing_arrival,
            "missing_departure": missing_departure,
        })
    
class OnboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for onboard module (confirmed bookings only).
    Owner, Manager, and Agent can access.
    """
    queryset = Booking.objects.filter(booking_status='confirmed')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, CanAccessBookings, AgencyDataIsolation]

    def get_queryset(self):
        """Filter confirmed bookings by agency"""
        user = self.request.user
        queryset = Booking.objects.filter(
            agency=user.agency,
            booking_status='confirmed'
        ).select_related('client', 'service', 'created_by')

        # ✅ Agent can only see his own confirmed bookings
        if user.role == 'agent':
            queryset = queryset.filter(created_by=user)

        # Filter by date range (safe with optional dates)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date:
            queryset = queryset.filter(arrival_date__isnull=False, arrival_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(departure_date__isnull=False, departure_date__lte=end_date)

        # Filter by payment status
        payment_status = self.request.query_params.get('payment_status', None)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        return queryset.order_by('arrival_date')


class AnalyticsView(views.APIView):
    """
    View for analytics data.
    Owner, Manager, and Accountant can access.
    Agent can access ONLY his own analytics (backend-filtered).
    """
    permission_classes = [IsAuthenticated, CanAccessAnalytics]

    def get(self, request):
        user = request.user

        # Get all bookings for the agency
        bookings = Booking.objects.filter(agency=user.agency)

        # ✅ Agent: only his own analytics
        if user.role == 'agent':
            bookings = bookings.filter(created_by=user)

        # ✅ NEW: Date Range Filters (lifetime/this_week/this_month/last_month/custom)
        range_filter = request.query_params.get('range', 'lifetime')
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        today = timezone.localdate()

        if range_filter == 'this_week':
            start = today - timezone.timedelta(days=today.weekday())
            end = start + timezone.timedelta(days=6)
            bookings = bookings.filter(created_at__date__gte=start, created_at__date__lte=end)

        elif range_filter == 'this_month':
            start = today.replace(day=1)
            bookings = bookings.filter(created_at__date__gte=start, created_at__date__lte=today)

        elif range_filter == 'last_month':
            first_this_month = today.replace(day=1)
            last_month_end = first_this_month - timezone.timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            bookings = bookings.filter(created_at__date__gte=last_month_start, created_at__date__lte=last_month_end)

        elif range_filter == 'custom':
            if start_date and end_date:
                bookings = bookings.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        # ✅ Calculate discount-adjusted total sales (DB level)
        total_sales_after_discount = bookings.aggregate(
            total=Sum(
                ExpressionWrapper(
                    (F('service__service_base_cost') + F('service__service_profit')) - F('discount'),
                    output_field=DecimalField(max_digits=12, decimal_places=2)
                )
            )
        )['total'] or Decimal('0.00')

        total_received = bookings.aggregate(
            total=Sum('paid_amount')
        )['total'] or Decimal('0.00')

        total_remaining = total_sales_after_discount - total_received

        # ✅ NEW: Total Profit
        total_profit = bookings.aggregate(
            total=Sum('service__service_profit')
        )['total'] or Decimal('0.00')

        # Payment breakdown
        payment_breakdown = {
            'paid': bookings.filter(payment_status='PAID').count(),
            'half_paid': bookings.filter(payment_status='HALF_PAID').count(),
            'pending': bookings.filter(payment_status='PENDING').count(),
        }

        # Agent trackers
        agent_bookings = bookings.values('created_by__username').annotate(
            count=Count('id')
        ).order_by('-count')

        agent_customers = bookings.values('created_by__username').annotate(
            unique_clients=Count('client', distinct=True)
        ).order_by('-unique_clients')

        # Total trackers
        total_bookings = bookings.count()
        total_customers = bookings.values('client').distinct().count()

        # Booking status breakdown
        booking_status_breakdown = {
            'pending': bookings.filter(booking_status='pending').count(),
            'confirmed': bookings.filter(booking_status='confirmed').count(),
            'rejected': bookings.filter(booking_status='rejected').count(),
        }

        return Response({
            'amounts': {
                'total_sales': str(total_sales_after_discount),
                'total_received': str(total_received),
                'total_remaining': str(total_remaining),
                'total_profit': str(total_profit),
            },
            'payment_breakdown': payment_breakdown,
            'booking_status_breakdown': booking_status_breakdown,
            'agent_bookings_tracker': list(agent_bookings),
            'agent_customers_tracker': list(agent_customers),
            'total_bookings': total_bookings,
            'total_customers': total_customers,
        })


class BookingNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing booking notes.
    """
    queryset = BookingNote.objects.all()
    serializer_class = BookingNoteSerializer
    permission_classes = [IsAuthenticated, CanAccessBookings]

    def get_queryset(self):
        """Filter notes by agency"""
        user = self.request.user
        return BookingNote.objects.filter(booking__agency=user.agency).order_by('-created_at')

    def perform_create(self, serializer):
        """Automatically set created_by when creating note"""
        serializer.save(created_by=self.request.user)
