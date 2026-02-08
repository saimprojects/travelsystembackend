# from django.db import models
# from django.core.validators import MinValueValidator
# from django.core.exceptions import ValidationError
# from decimal import Decimal


# class Booking(models.Model):
#     """
#     Booking model for client bookings with payment tracking.
#     """
#     BOOKING_STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('rejected', 'Rejected'),
#     ]

#     PAYMENT_STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('HALF_PAID', 'Half Paid'),
#         ('PAID', 'Paid'),
#     ]

#     agency = models.ForeignKey(
#         'agencies.Agency',
#         on_delete=models.CASCADE,
#         related_name='bookings'
#     )
#     client = models.ForeignKey(
#         'clients.Client',
#         on_delete=models.CASCADE,
#         related_name='bookings'
#     )
#     service = models.ForeignKey(
#         'services.Service',
#         on_delete=models.CASCADE,
#         related_name='bookings'
#     )
#     discount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=Decimal('0.00'),
#         validators=[MinValueValidator(Decimal('0.00'))]
#     )
#     booking_status = models.CharField(
#         max_length=20,
#         choices=BOOKING_STATUS_CHOICES,
#         default='pending'
#     )

#     # Payment fields
#     paid_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=Decimal('0.00'),
#         validators=[MinValueValidator(Decimal('0.00'))]
#     )
#     payment_status = models.CharField(
#         max_length=20,
#         choices=PAYMENT_STATUS_CHOICES,
#         default='PENDING'
#     )
#     payment_method = models.CharField(max_length=100, blank=True, null=True)
#     last_payment_date = models.DateTimeField(blank=True, null=True)

#     # Onboard fields (✅ optional)
#     arrival_date = models.DateField(blank=True, null=True)
#     departure_date = models.DateField(blank=True, null=True)

#     created_by = models.ForeignKey(
#         'users.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='created_bookings'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Booking'
#         verbose_name_plural = 'Bookings'
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Booking #{self.id} - {self.client.name} - {self.service.service_name}"

#     @property
#     def total_amount(self):
#         """Calculate total amount after discount"""
#         return self.service.service_total_price - self.discount

#     @property
#     def remaining_amount(self):
#         """Calculate remaining amount to be paid"""
#         return self.total_amount - self.paid_amount

#     def update_payment_status(self):
#         """Auto-update payment status based on paid amount"""
#         if self.paid_amount == 0:
#             self.payment_status = 'PENDING'
#         elif self.paid_amount >= self.total_amount:
#             self.payment_status = 'PAID'
#         else:
#             self.payment_status = 'HALF_PAID'

#     def clean(self):
#         """Validate discount rules + date rules (dates optional)"""
#         if self.service:
#             max_discount = self.service.service_profit * Decimal('0.50')  # 50% of profit

#             if self.discount > max_discount:
#                 raise ValidationError({
#                     'discount': f'Discount cannot exceed 50% of profit (max: {max_discount})'
#                 })

#             # Ensure discount doesn't reduce price below base cost
#             if self.total_amount < self.service.service_base_cost:
#                 raise ValidationError({
#                     'discount': 'Discount cannot reduce price below base cost'
#                 })

#         # ✅ Dates are optional: only validate order if BOTH provided
#         if self.departure_date and self.arrival_date:
#             if self.arrival_date < self.departure_date:
#                 raise ValidationError({
#                     'arrival_date': 'Arrival date cannot be before departure date.'
#                 })

#     def save(self, *args, **kwargs):
#         self.update_payment_status()
#         self.full_clean()
#         super().save(*args, **kwargs)

# class BookingNote(models.Model):
#     """
#     Notes for bookings with date tracking.
#     """
#     booking = models.ForeignKey(
#         Booking,
#         on_delete=models.CASCADE,
#         related_name='notes'
#     )
#     note = models.TextField()
#     created_by = models.ForeignKey(
#         'users.User',
#         on_delete=models.SET_NULL,
#         null=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Booking Note'
#         verbose_name_plural = 'Booking Notes'
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Note for Booking #{self.booking.id} - {self.created_at.strftime('%Y-%m-%d')}"


from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class Booking(models.Model):
    """
    Booking model for client bookings with payment tracking.
    """
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('HALF_PAID', 'Half Paid'),
        ('PAID', 'Paid'),
    ]

    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS_CHOICES,
        default='pending'
    )

    # Payment fields
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    last_payment_date = models.DateTimeField(blank=True, null=True)

    # Travel dates (✅ optional)
    departure_date = models.DateField(blank=True, null=True)  # Travel date - when client leaves
    arrival_date = models.DateField(blank=True, null=True)    # Return date - when client comes back

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_bookings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.client.name} - {self.service.service_name}"

    @property
    def total_amount(self):
        """Calculate total amount after discount"""
        return self.service.service_total_price - self.discount

    @property
    def remaining_amount(self):
        """Calculate remaining amount to be paid"""
        return self.total_amount - self.paid_amount

    def update_payment_status(self):
        """Auto-update payment status based on paid amount"""
        if self.paid_amount == 0:
            self.payment_status = 'PENDING'
        elif self.paid_amount >= self.total_amount:
            self.payment_status = 'PAID'
        else:
            self.payment_status = 'HALF_PAID'

    def clean(self):
        """Validate discount rules + date rules (dates optional)"""
        if self.service:
            max_discount = self.service.service_profit * Decimal('0.50')  # 50% of profit

            if self.discount > max_discount:
                raise ValidationError({
                    'discount': f'Discount cannot exceed 50% of profit (max: {max_discount})'
                })

            # Ensure discount doesn't reduce price below base cost
            if self.total_amount < self.service.service_base_cost:
                raise ValidationError({
                    'discount': 'Discount cannot reduce price below base cost'
                })

        # ✅ TRAVEL LOGIC: DEPARTURE DATE (travel) first, then ARRIVAL DATE (return)
        # Return date must be AFTER travel date
        if self.departure_date and self.arrival_date:
            if self.arrival_date < self.departure_date:
                raise ValidationError({
                    'arrival_date': 'Return date must be after travel date'
                })

    def save(self, *args, **kwargs):
        self.update_payment_status()
        self.full_clean()
        super().save(*args, **kwargs)


class BookingNote(models.Model):
    """
    Notes for bookings with date tracking.
    """
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note = models.TextField()
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Booking Note'
        verbose_name_plural = 'Booking Notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for Booking #{self.booking.id} - {self.created_at.strftime('%Y-%m-%d')}"