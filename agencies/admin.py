from django.contrib import admin
from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Agency Information', {
            'fields': ('name', 'logo', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
