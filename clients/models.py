from django.db import models


class Client(models.Model):
    """
    Client model for customers of travel agencies.
    """
    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.CASCADE,
        related_name='clients'
    )
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    alternative_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    cnic = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_clients'
    )
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class ClientNote(models.Model):
    """
    Notes for clients with date tracking.
    """
    client = models.ForeignKey(
        Client,
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
        verbose_name = 'Client Note'
        verbose_name_plural = 'Client Notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.client.name} - {self.created_at.strftime('%Y-%m-%d')}"
