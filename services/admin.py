from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'agency', 'destination', 'service_total_price', 'status', 'created_at']
    list_filter = ['status', 'agency', 'created_at']
    search_fields = ['service_name', 'destination']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('agency', 'service_name', 'destination', 'service_duration', 'status')
        }),
        ('Pricing', {
            'fields': ('service_base_cost', 'service_profit')
        }),
        ('Inclusions', {
            'fields': ('service_include',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
