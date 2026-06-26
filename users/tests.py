from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from agencies.models import Agency
from users.models import User


class LoginViewTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.agency = Agency.objects.create(
            name='Demo Agency',
            email='agency@example.com',
            status='active',
        )
        self.user = User.objects.create_user(
            username='demo',
            email='demo@example.com',
            password='correct-password',
            agency=self.agency,
            role='agency_owner',
        )

    def test_invalid_credentials_return_401_not_500(self):
        response = self.client.post(
            self.login_url,
            {'email': self.user.email, 'password': 'wrong-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_missing_email_returns_400_not_500(self):
        response = self.client.post(
            self.login_url,
            {'password': 'correct-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_inactive_agency_returns_403(self):
        self.agency.status = 'suspended'
        self.agency.save(update_fields=['status'])

        response = self.client.post(
            self.login_url,
            {'email': self.user.email, 'password': 'correct-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['agency_status'], 'suspended')

    def test_active_agency_login_returns_tokens(self):
        response = self.client.post(
            self.login_url,
            {'email': self.user.email, 'password': 'correct-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
