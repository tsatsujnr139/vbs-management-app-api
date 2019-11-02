from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Parent
from participant.serializers import ParentSerializer

PARENT_URL = reverse('participant:parent-list')


class ParentApiTests(TestCase):
    """Test for parent api"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_parents(self):
        """Test retrieve parents api"""
        Parent.objects.create(full_name='Aforo Asomaning',
                              primary_contact_no='0244123456',
                              alternate_contact_no='0544123456')
        Parent.objects.create(
            full_name='Kafui Yeboah',
            primary_contact_no='0244123456',
            alternate_contact_no='0544123456'
        )
        parents = Participant.objects.all().order_by('id')
        res = self.client.get(PARENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ParentSerializer(parents, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_add_parent_successfully(self):
        """Test add parent successfully"""
        payload = {
            'full_name': 'Aforo Asomaning',
            'primary_contact_no': '0244123456',
            'alternate_contact_no': '0544123456'
        }
        res = self.client.post(PARENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        parent_exists = Parent.objects.filter(
            full_name=payload['full_name']).exists
        self.assertTrue(parent_exists)

    def test_add_parent_invalid_payload(self):
        """Test adding parent invalid payload fails"""
        res = self.client.post(PARENT_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_parent_missing_name(self):
        """Test adding parent with missing name fails"""
        payload = {
            'full_name': '',
            'primary_contact_no': '0244123456',
            'alternate_contact_no': '0544123456'
        }
        res = self.client.post(PARENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_parent_missing_primary_contact_no(self):
        """Test adding parent with missing name fails"""
        payload = {
            'full_name': 'Aforo Asomaning',
            'primary_contact_no': '',
            'alternate_contact_no': '0544123456'
        }
        res = self.client.post(PARENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_parent_missing_alternate_contact_no(self):
        """Test adding parent with missing name fails"""
        payload = {
            'full_name': 'Aforo Asomaning',
            'primary_contact_no': '0544123456',
            'alternate_contact_no': ''
        }
        res = self.client.post(PARENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
