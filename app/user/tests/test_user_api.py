from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """create a user"""
    return get_user_model().objects.create_user(**params)


def sample_user():
    return {
        'email': 'user@email.com',
        'password': 'password123',
        'name': 'test name'
    }


class PublicUserTests(TestCase):
    """test publicly accessible api's"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successfully(self):
        """test creating an user with valid payload successfully"""
        payload = sample_user()

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_invalid_payload(self):
        """test creating a user with invalid payload fails"""

        payload = {
            'email': '',
            'password': ''
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_exists(self):
        """test creating user that already exists fails"""
        payload = sample_user()
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test creating user with password less than 5 characters fails """
        payload = {
            'email': 'user@email.com',
            'password': 'pass'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
