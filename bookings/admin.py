from django.contrib import admin
from .models import Booking, BookingNote


class BookingNoteInline(admin.TabularInline):
    model = BookingNote
    extra = 0
    readonly_fields = ['created_at', 'created_by']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'service', 'agency', 'booking_status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['booking_status', 'payment_status', 'agency', 'created_at']
    search_fields = ['client__name', 'service__service_name']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'total_amount', 'remaining_amount']
    inlines = [BookingNoteInline]
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('agency', 'client', 'service', 'booking_status')
        }),
        ('Pricing & Discount', {
            'fields': ('discount', 'total_amount')
        }),
        ('Payment Information', {
            'fields': ('paid_amount', 'remaining_amount', 'payment_status', 'payment_method', 'last_payment_date')
        }),
        ('Onboard Details', {
            'fields': ('arrival_date', 'departure_date')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BookingNote)
class BookingNoteAdmin(admin.ModelAdmin):
    list_display = ['booking', 'note', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['booking__client__name', 'note']
    readonly_fields = ['created_at']
