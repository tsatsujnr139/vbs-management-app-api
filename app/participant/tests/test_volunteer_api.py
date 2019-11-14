from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Volunteer, Church

from participant.serializers import VolunteerSerializer


VOLUNTEER_URL = reverse('participant:volunteer-list')
VOLUNTEER_COUNT_URL = reverse('participant:volunteer-count')


def sample_church(name='Legon Interdenominational Church'):
    return Church.objects.create(
        name=name
    )


def get_detail_url(volunteer_id):
    """return volunteer detail URL"""
    return reverse('participant:volunteer-detail',
                   kwargs={'id': volunteer_id}
                   )


class VolunteerTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_volunteers_for_authorized_user(self):
        """Test retrieval of volunteer list for authorized user """

        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'password'
        )
        self.client.force_authenticate(self.user)

        Volunteer.objects.create(
            first_name='Tsatsu',
            last_name='Adogla-Bessa',
            role='Teaching',
            contact_no='0500018351',
            email='tsatsujnr@gmail.com',
            gender='Male',
            preferred_class='Pre-School',
            church=sample_church(),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        Volunteer.objects.create(
            first_name='Hetty',
            last_name='Yirenkyi-Boafo',
            role='Teaching',
            contact_no='0243578943',
            email='hetty@gmail.com',
            gender='Female',
            preferred_class='Class 1',
            church=sample_church(name='Anglican Church'),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        res = self.client.get(VOLUNTEER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        volunteers = Volunteer.objects.all().order_by('id')
        serializer = VolunteerSerializer(volunteers, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_volunteers_for_unauthorized_user(self):
        """Test retrieval of volunteer list for unauthorized user """
        Volunteer.objects.create(
            first_name='Tsatsu',
            last_name='Adogla-Bessa',
            role='Teaching',
            contact_no='0500018351',
            email='tsatsujnr@gmail.com',
            gender='Male',
            preferred_class='Pre-School',
            church=sample_church(),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        Volunteer.objects.create(
            first_name='Hetty',
            last_name='Yirenkyi-Boafo',
            role='Teaching',
            contact_no='0243578943',
            email='hetty@gmail.com',
            gender='Female',
            preferred_class='Class 1',
            church=sample_church(name='Anglican Church'),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        res = self.client.get(VOLUNTEER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_volunteer(self):
        """Test adding a new volunteer"""

        payload = {
            'first_name': 'Tsatsu',
            'last_name': 'Adogla-Bessa',
            'role': 'Teaching',
            'contact_no': '0500018351',
            'email': 'tsatsujnr@gmail.com',
            'gender': 'Male',
            'preferred_class': 'Pre-School',
            'church': sample_church().id,
            'previous_volunteer': 1,
            'previous_site': 'Pre-School'
        }

        res = self.client.post(VOLUNTEER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        volunteer_exists = Volunteer.objects.filter(
            first_name='Tsatsu', last_name='Adogla-Bessa'
        ).exists
        self.assertTrue(volunteer_exists)

    def test_add_volunteer_invalid_payload(self):
        """Test adding a new volunteer with invalid payload failsw"""

        payload = {
            'first_name': 'Tsatsu',
            'last_name': '',
            'role': 'Teaching',
            'contact_no': '0500018351',
            'email': 'tsatsujnr@gmail.com',
            'gender': 'Male',
            'preferred_class': 'Pre-School',
            'church': sample_church().id,
            'previous_volunteer': 1,
            'previous_site': 'Pre-School'
        }

        res = self.client.post(VOLUNTEER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_volunteer_details_for_authorized_user(self):
        """Test view specific volunteer details for authorized user"""
        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'password'
        )
        self.client.force_authenticate(self.user)

        volunteer = Volunteer.objects.create(
            first_name='Hetty',
            last_name='Yirenkyi-Boafo',
            role='Teaching',
            contact_no='0243578943',
            email='hetty@gmail.com',
            gender='Female',
            preferred_class='Class 1',
            church=sample_church(),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        url = get_detail_url(volunteer.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], volunteer.first_name)

    def test_view_volunteer_details_for_unauthorized_user(self):
        """Test view specific volunteer details for unauthorized user"""

        volunteer = Volunteer.objects.create(
            first_name='Hetty',
            last_name='Yirenkyi-Boafo',
            role='Teaching',
            contact_no='0243578943',
            email='hetty@gmail.com',
            gender='Female',
            preferred_class='Class 1',
            church=sample_church(),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        url = get_detail_url(volunteer.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_volunteer_count(self):
        """Test retrieve volunteer count api"""
        Volunteer.objects.create(
            first_name='Tsatsu',
            last_name='Adogla-Bessa',
            role='Teaching',
            contact_no='0500018351',
            email='tsatsujnr@gmail.com',
            gender='Male',
            preferred_class='Pre-School',
            church=sample_church(),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        Volunteer.objects.create(
            first_name='Hetty',
            last_name='Yirenkyi-Boafo',
            role='Teaching',
            contact_no='0243578943',
            email='hetty@gmail.com',
            gender='Female',
            preferred_class='Class 1',
            church=sample_church(name='Anglican Church'),
            previous_volunteer=True,
            previous_site='Pre-School'
        )

        res = self.client.get(VOLUNTEER_COUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)
