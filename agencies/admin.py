from django.contrib import admin
from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'advanced_features_enabled', 'created_at']
    list_filter = ['status', 'advanced_features_enabled', 'created_at']
    list_editable = ['advanced_features_enabled']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Agency Information', {
            'fields': ('name', 'logo', 'status', 'phone_number', 'email', 'address', 'description')
        }),
        ('Invoice Settings', {
            'fields': ('invoice_template',)
        }),
        ('Advanced Features', {
            'fields': ('advanced_features_enabled',),
            'description': 'Enable advanced features like Visa & Ticket management for this agency.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
