from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Service(models.Model):
    """
    Service model for travel packages offered by agencies.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.CASCADE,
        related_name='services'
    )
    service_name = models.CharField(max_length=255)
    service_include = models.JSONField(default=list, help_text="List of inclusions")
    service_base_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    service_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    service_duration = models.CharField(max_length=100, help_text="e.g., 5 days, 2 weeks")
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service_name} - {self.destination}"
    
    @property
    def service_total_price(self):
        """Calculate total price (base cost + profit)"""
        return self.service_base_cost + self.service_profit
