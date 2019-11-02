from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Church
from participant.serializers import ChurchSerializer


CHURCHES_URL = reverse('participant:church-list')


class ChurchApiTests(TestCase):
    """tests church api's"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_churches_successfully(self):
        """test retrieve all churches successfully"""

        Church.objects.create(
            name='Legon Interdenominational Church')
        Church.objects.create(name='Christ Anglican Church')

        churches = Church.objects.all().order_by('id')
        serializer = ChurchSerializer(churches, many=True)
        res = self.client.get(CHURCHES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_add_church(self):
        """test adding a new church"""
        payload = {
            'name': 'Legon Interdenominational Church'
        }
        res = self.client.post(CHURCHES_URL, payload)
        church_exists = Church.objects.filter(name=payload['name']).exists
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(church_exists)

    def test_add_church_invalid_payload(self):
        """test grade with invalid payload fails"""

        res = self.client.post(CHURCHES_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
