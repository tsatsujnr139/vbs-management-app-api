from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import PickupPerson
from participant.serializers import PickupPersonSerializer


PICKUP_PERSON_URL = reverse('participant:pickupperson-list')


class PickupPersonApiTests(TestCase):
    """Tests for pickup person api"""

    def setUp(self):
        self.client = APIClient()

    def test_retreive_pickup_persons_successfully(self):
        """Test retrieval of pick up person successfully"""

        PickupPerson.objects.create(
            full_name='Aforo Asomaning', contact_no='0244123456')
        PickupPerson.objects.create(
            full_name='Kafui Yeboah', contact_no='0544123456')

        res = self.client.get(PICKUP_PERSON_URL)
        pickuppeople = PickupPerson.objects.all().order_by('id')
        serializer = PickupPersonSerializer(pickuppeople, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_add_new_pickup_person(self):
        """test add new pickup person successfully"""

        payload = {
            'full_name': 'Aforo Asomaning',
            'contact_no': '0244123456'
        }

        res = self.client.post(PICKUP_PERSON_URL, payload)
        person_exists = PickupPerson.objects.filter(
            full_name=payload['full_name']).exists
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(person_exists)

    def test_add_pickup_person_invalid_payload(self):
        """test adding pickup person with invalid payload fails"""

        res = self.client.post(PICKUP_PERSON_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
