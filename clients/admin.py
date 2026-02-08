from django.contrib import admin
from .models import Client, ClientNote


class ClientNoteInline(admin.TabularInline):
    model = ClientNote
    extra = 0
    readonly_fields = ['created_at', 'created_by']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency', 'phone_number', 'email', 'created_at']
    list_filter = ['agency', 'created_at']
    search_fields = ['name', 'phone_number', 'email', 'passport_number', 'cnic']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    inlines = [ClientNoteInline]
    
    fieldsets = (
        ('Client Information', {
            'fields': ('agency', 'name', 'email')
        }),
        ('Contact Details', {
            'fields': ('phone_number', 'alternative_number', 'address')
        }),
        ('Identification', {
            'fields': ('passport_number', 'cnic')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClientNote)
class ClientNoteAdmin(admin.ModelAdmin):
    list_display = ['client', 'note', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['client__name', 'note']
    readonly_fields = ['created_at']
