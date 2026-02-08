from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control.
    """
    ROLE_CHOICES = [
        ('super_user', 'Super User'),
        ('agency_owner', 'Agency Owner'),
        ('manager', 'Manager'),
        ('agent', 'Agent'),
        ('accountant', 'Accountant'),
    ]

    # ✅ Email-based login support
    email = models.EmailField(unique=True)

    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ Use email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"

    @property
    def is_super_user_role(self):
        return self.role == 'super_user'

    @property
    def is_agency_owner(self):
        return self.role == 'agency_owner'

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_agent(self):
        return self.role == 'agent'

    @property
    def is_accountant(self):
        return self.role == 'accountant'

    @property
    def can_manage_settings(self):
        return self.role in ['agency_owner', 'manager']

    @property
    def can_view_analytics(self):
        return self.role in ['agency_owner', 'manager', 'accountant']
