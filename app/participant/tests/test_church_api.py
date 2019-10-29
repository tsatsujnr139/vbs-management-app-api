from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Church
from participant.serializers import ChurchSerializer


CHURCHES_URL = reverse('participant:church-list')


class ChurchTests(TestCase):
    """tests church api's"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_churches_successfully(self):
        """test retrieve all churches successfully"""

        church1 = Church.objects.create(
            name='Legon Interdenominational Church')
        church2 = Church.objects.create(name='Christ Anglican Church')

        res = self.client.get(CHURCHES_URL)
        churches = Church.objects.all().order_by('id')
        serializer = ChurchSerializer(churches, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer)

    def test_add_church(self):
        """test adding a new church"""
        payload = {
            'name': 'Legon Interdenominational Church'
        }
        res = self.client.post(CHURCHES_URL, payload)
        church_exists = Church.objects.filter(name=payload['name']).exists
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(church_exists)
