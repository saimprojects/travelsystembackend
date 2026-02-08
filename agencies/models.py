from django.db import models
from cloudinary.models import CloudinaryField


class Agency(models.Model):
    """
    Agency model representing a travel agency in the SaaS system.
    Each agency has its own isolated data.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('locked', 'Locked'),
        ('pending', 'Pending'),
    ]
    
    # ✅ EXISTING FIELDS
    name = models.CharField(max_length=255)
    logo = CloudinaryField('agency_logo', blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ✅ ADD THESE FIELDS FOR SERIALIZER
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        """Check if agency is active"""
        return self.status == 'active'
    
    def get_status_display(self):
        """Get human-readable status"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    # ✅ ADD THIS METHOD FOR logo_url
    @property
    def logo_url(self):
        """Get logo URL"""
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return None