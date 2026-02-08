# from rest_framework import serializers
# from decimal import Decimal
# from .models import Booking, BookingNote
# from clients.serializers import ClientSerializer
# from services.serializers import ServiceSerializer, ServiceAgentSerializer


# class BookingNoteSerializer(serializers.ModelSerializer):
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)

#     class Meta:
#         model = BookingNote
#         fields = ['id', 'booking', 'note', 'created_by', 'created_by_name', 'created_at']
#         read_only_fields = ['id', 'created_by', 'created_at']


# class BookingSerializer(serializers.ModelSerializer):
#     client_details = ClientSerializer(source='client', read_only=True)
#     service_details = ServiceSerializer(source='service', read_only=True)
#     notes = BookingNoteSerializer(many=True, read_only=True)
#     total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     booking_status_display = serializers.CharField(source='get_booking_status_display', read_only=True)
#     payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
#     created_by_name = serializers.CharField(source='created_by.username', read_only=True)

#     class Meta:
#         model = Booking
#         fields = [
#             'id', 'agency', 'client', 'client_details', 'service', 'service_details',
#             'discount', 'booking_status', 'booking_status_display',
#             'paid_amount', 'total_amount', 'remaining_amount',
#             'payment_status', 'payment_status_display', 'payment_method', 'last_payment_date',
#             'arrival_date', 'departure_date', 'notes',
#             'created_by', 'created_by_name', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'agency', 'created_by', 'payment_status', 'created_at', 'updated_at']


# class BookingCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = [
#             'client', 'service', 'discount', 'booking_status',
#             'paid_amount', 'payment_method', 'last_payment_date',
#             'arrival_date', 'departure_date'
#         ]

#     def validate(self, data):
#         """Validate discount rules + optional date rules"""
#         service = data.get('service')
#         discount = data.get('discount', Decimal('0.00'))

#         # ensure Decimal type
#         if discount is None:
#             discount = Decimal('0.00')

#         if service and discount:
#             profit = service.service_profit or Decimal('0.00')
#             max_discount = profit * Decimal('0.50')

#             if discount > max_discount:
#                 raise serializers.ValidationError({
#                     'discount': f'Discount cannot exceed 50% of profit (max: {max_discount})'
#                 })

#             total_after_discount = service.service_total_price - discount
#             if total_after_discount < service.service_base_cost:
#                 raise serializers.ValidationError({
#                     'discount': 'Discount cannot reduce price below base cost'
#                 })

#         # ✅ Dates optional: only validate order if BOTH provided
#         arrival_date = data.get('arrival_date')
#         departure_date = data.get('departure_date')
#         if arrival_date and departure_date and departure_date < arrival_date:
#             raise serializers.ValidationError({
#                 'departure_date': 'Departure date cannot be before arrival date.'
#             })

#         return data


# class BookingUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = [
#             'discount', 'booking_status', 'paid_amount', 'payment_method',
#             'last_payment_date', 'arrival_date', 'departure_date'
#         ]

#     def validate(self, data):
#         """Validate discount rules on update + optional date rules"""
#         instance = self.instance
#         service = instance.service
#         discount = data.get('discount', instance.discount)

#         # ensure Decimal type
#         if discount is None:
#             discount = Decimal('0.00')

#         if discount:
#             profit = service.service_profit or Decimal('0.00')
#             max_discount = profit * Decimal('0.50')

#             if discount > max_discount:
#                 raise serializers.ValidationError({
#                     'discount': f'Discount cannot exceed 50% of profit (max: {max_discount})'
#                 })

#             total_after_discount = service.service_total_price - discount
#             if total_after_discount < service.service_base_cost:
#                 raise serializers.ValidationError({
#                     'discount': 'Discount cannot reduce price below base cost'
#                 })

#         # ✅ Dates optional: only validate order if BOTH provided
#         arrival_date = data.get('arrival_date', instance.arrival_date)
#         departure_date = data.get('departure_date', instance.departure_date)
#         if arrival_date and departure_date and departure_date < arrival_date:
#             raise serializers.ValidationError({
#                 'departure_date': 'Departure date cannot be before arrival date.'
#             })

#         return data


# class BookingAgentSerializer(serializers.ModelSerializer):
#     """Serializer for agents with limited service details"""
#     client_details = ClientSerializer(source='client', read_only=True)
#     service_details = ServiceAgentSerializer(source='service', read_only=True)
#     total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     booking_status_display = serializers.CharField(source='get_booking_status_display', read_only=True)
#     payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

#     class Meta:
#         model = Booking
#         fields = [
#             'id', 'client', 'client_details', 'service', 'service_details',
#             'discount', 'booking_status', 'booking_status_display',
#             'paid_amount', 'total_amount', 'remaining_amount',
#             'payment_status', 'payment_status_display', 'payment_method', 'last_payment_date',
#             'arrival_date', 'departure_date', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'payment_status', 'created_at', 'updated_at']



from rest_framework import serializers
from decimal import Decimal
from .models import Booking, BookingNote
from clients.serializers import ClientSerializer
from services.serializers import ServiceSerializer, ServiceAgentSerializer


class BookingNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = BookingNote
        fields = ['id', 'booking', 'note', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    notes = BookingNoteSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    booking_status_display = serializers.CharField(source='get_booking_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'agency', 'client', 'client_details', 'service', 'service_details',
            'discount', 'booking_status', 'booking_status_display',
            'paid_amount', 'total_amount', 'remaining_amount',
            'payment_status', 'payment_status_display', 'payment_method', 'last_payment_date',
            'departure_date', 'arrival_date', 'notes',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'agency', 'created_by', 'payment_status', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'client', 'service', 'discount', 'booking_status',
            'paid_amount', 'payment_method', 'last_payment_date',
            'departure_date', 'arrival_date'
        ]

    def validate(self, data):
        """Validate discount rules + travel date logic"""
        service = data.get('service')
        discount = data.get('discount', Decimal('0.00'))

        # ensure Decimal type
        if discount is None:
            discount = Decimal('0.00')

        if service and discount:
            profit = service.service_profit or Decimal('0.00')
            max_discount = profit * Decimal('0.50')

            if discount > max_discount:
                raise serializers.ValidationError({
                    'discount': f'Discount cannot exceed 50% of profit (max: {max_discount})'
                })

            total_after_discount = service.service_total_price - discount
            if total_after_discount < service.service_base_cost:
                raise serializers.ValidationError({
                    'discount': 'Discount cannot reduce price below base cost'
                })

        # ✅ TRAVEL LOGIC: Return date (arrival) must be AFTER travel date (departure)
        departure_date = data.get('departure_date')
        arrival_date = data.get('arrival_date')
        
        if departure_date and arrival_date:
            if arrival_date < departure_date:
                raise serializers.ValidationError({
                    'arrival_date': 'Return date must be after travel date'
                })

        return data


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'discount', 'booking_status', 'paid_amount', 'payment_method',
            'last_payment_date', 'departure_date', 'arrival_date'
        ]

    def validate(self, data):
        """Validate discount rules on update + travel date logic"""
        instance = self.instance
        service = instance.service
        discount = data.get('discount', instance.discount)

        # ensure Decimal type
        if discount is None:
            discount = Decimal('0.00')

        if discount:
            profit = service.service_profit or Decimal('0.00')
            max_discount = profit * Decimal('0.50')

            if discount > max_discount:
                raise serializers.ValidationError({
                    'discount': f'Discount cannot exceed 50% of profit (max: {max_discount})'
                })

            total_after_discount = service.service_total_price - discount
            if total_after_discount < service.service_base_cost:
                raise serializers.ValidationError({
                    'discount': 'Discount cannot reduce price below base cost'
                })

        # ✅ TRAVEL LOGIC: Return date (arrival) must be AFTER travel date (departure)
        departure_date = data.get('departure_date', instance.departure_date)
        arrival_date = data.get('arrival_date', instance.arrival_date)
        
        if departure_date and arrival_date:
            if arrival_date < departure_date:
                raise serializers.ValidationError({
                    'arrival_date': 'Return date must be after travel date'
                })

        return data


class BookingAgentSerializer(serializers.ModelSerializer):
    """Serializer for agents with limited service details"""
    client_details = ClientSerializer(source='client', read_only=True)
    service_details = ServiceAgentSerializer(source='service', read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    booking_status_display = serializers.CharField(source='get_booking_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'client', 'client_details', 'service', 'service_details',
            'discount', 'booking_status', 'booking_status_display',
            'paid_amount', 'total_amount', 'remaining_amount',
            'payment_status', 'payment_status_display', 'payment_method', 'last_payment_date',
            'departure_date', 'arrival_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'payment_status', 'created_at', 'updated_at']