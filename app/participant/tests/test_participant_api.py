from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Participant, Grade,
                         Church)
from participant.serializers import ParticipantSerializer


PARTICIPANT_URL = reverse('participant:participant-list')


def sample_church(name='Legon Interdenominational Church'):
    return Church.objects.create(
        name=name
    )


def sample_grade(name='Class 1'):
    return Grade.objects.create(
        name=name
    )


def sample_participant(**params):

    defaults = {
        'first_name': 'Adoma',
        'last_name': 'Asomaning',
        'age': 8,
        'date_of_birth': '2004-01-01',
        'gender': 'Female',
        'church': 'Legon interdenominational Church',
        'parent_name': "Aforo Asomaning",
        'primary_contact_no': '0244123456',
        'alternate_contact_no': '0244123456',
        'email': 'aforo@gmail.com',
        'pickup_person_name': 'Aforo Asomaning',
        'pickup_person_contact_no': '0244123456',
        'medical_info': 'Allergic to pineapple'
    }

    defaults.update(params)

    return Participant.objects.create(**defaults)


def get_detail_url(participant_id):
    """return participant detail URL"""
    return reverse('participant:participant-detail',
                   kwargs={'id': participant_id}
                   )


class ParticipantsApiTests(TestCase):
    """Tests for participant API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_participants_for_authenticated_user(self):
        """Test retrieving participant list successfully"""
        self.user = get_user_model().objects.create_user(
            'user@company.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

        Participant.objects.create(
            first_name='Adoma',
            last_name='Asomaning',
            date_of_birth='2003-01-01'
        )

        Participant.objects.create(
            first_name='Aba',
            last_name='Asomaning',
            date_of_birth='2000-01-01'
        )

        participants = Participant.objects.all().order_by('id')
        res = self.client.get(PARTICIPANT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ParticipantSerializer(participants, many=True)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_participants_unauthorized_user(self):
        """test retrieve participant list for unauthorized user"""
        res = self.client.get(PARTICIPANT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_participant(self):
        """Test add new participant succesfully"""

        payload = {
            'first_name': 'Aba ',
            'last_name': 'Asomaning',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'age': 8,
            'grade': 'Class 1',
            'church': 'Legon Interdenominational Church',
            'parent_name': "Aforo Asomaning",
            'primary_contact_no': '0244123456',
            'whatsApp_no': '0244123456',
            'alternate_contact_no': '0244123456',
            'email': 'aforo@gmail.com',
            'pickup_person_name': 'Aforo Asomaning',
            'pickup_person_contact_no': '0244123456'
        }

        res = self.client.post(PARTICIPANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        participant_created = Participant.objects.filter(
            first_name='Aba', last_name='Asomaning').exists
        self.assertTrue(participant_created)

    def test_view_participant_details_for_authenticated_user(self):
        """Test viewing a specific participant detail for authenticated user"""
        self.user = get_user_model().objects.create_user(
            'user@company.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

        participant = sample_participant()

        url = get_detail_url(participant.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], participant.first_name)

    def test_view_participant_details_for_unauthorized_user(self):
        """
        Test viewing a specific participant detail for unauthorized user fails

        """

        participant = sample_participant()

        url = get_detail_url(participant.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_participant_list_by_class(self):
        """Test retrieving participant list by class api"""

        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

        payload1 = {
            'first_name': 'Ewurabena',
            'last_name': 'Surname',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': 'Class 1',
            'age': 8,
            'church': 'Legon Interdenominational Church',
            'parent_name': "Aforo Asomaning",
            'primary_contact_no': '0244123456',
            'whatsApp_no': '0244123456',
            'alternate_contact_no': '0244123456',
            'email': 'aforo@gmail.com',
            'pickup_person_name': 'Aforo Asomaning',
            'pickup_person_contact_no': '0244123456'
        }

        payload2 = {
            'first_name': 'Aba',
            'last_name': 'Asomaning',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': 'JHS 1',
            'age': 11,
            'church': 'Legon Interdenominational Church',
            'parent_name': "Aforo Asomaning",
            'primary_contact_no': '0244123456',
            'whatsApp_no': '0244123456',
            'alternate_contact_no': '0244123456',
            'email': 'aforo@gmail.com',
            'pickup_person_name': 'Aforo Asomaning',
            'pickup_person_contact_no': '0244123456'
        }

        payload3 = {
            'first_name': 'Owusua',
            'last_name': 'Yeboah',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': 'Class 1',
            'age': 8,
            'church': 'Legon Interdenominational Church',
            'parent_name': "Kafui Yeboah",
            'primary_contact_no': '0244123456',
            'whatsApp_no': '0244123456',
            'alternate_contact_no': '0244123456',
            'email': 'aforo@gmail.com',
            'pickup_person_name': 'Kafui Yeboah',
            'pickup_person_contact_no': '0244123456'
        }

        self.client.post(PARTICIPANT_URL, payload1)
        self.client.post(PARTICIPANT_URL, payload2)
        self.client.post(PARTICIPANT_URL, payload3)

        res = self.client.get(PARTICIPANT_URL, {'grade': 'Class 1'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[1]['first_name'], payload3['first_name'])
