from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Participant, Grade,
                         Church, PickupPerson,
                         Parent)
from participant.serializer import ParticipantSerializer, ParticipantDetailSerializer


PARTICIPANT_URL = reverse('participant:participant-list')


def sample_parent(**params):

    defaults = {
        'full_name': 'Aforo Asomaning',
        'primary_contact_no': '0244123456',
        'alternate_contact_no': '0255123456'
    }

    defaults.update(params)

    return models.Parent.objects.create(
        full_name=full_name,
        primary_contact_no=primary_contact_no,
        alternate_contact_no=alternate_contact_no
    )


def sample_pickup_person(full_name='Aforo',
                         contact_no='0244123456'):
    return models.PickupPerson.objects.create(
        full_name=full_name,
        contact_no=contact_no
    )


def sample_church(name='Legon Interdenominational Church'):
    return models.Church.objects.create(
        name=name
    )


def sample_grade(name='Class1'):
    return models.Grade.objects.create(
        name=name
    )


def sample_participant(grade, church, pickup_person, parent, **params):

    defaults = {
        'first_name': 'Adoma ',
        'last_name': 'Asomaning',
        'date_of_birth': '2004-01-01',
        'gender': 'Female',
        'medical_info': 'Allergic to pineapple'
    }

    defaults.update(params)

    return Participant.objects.create(grade=grade,
                                      church=church,
                                      pickup_person=pickup_person,
                                      parent=parent,
                                      **defaults)


def get_detail_url(participant_id):
    """return participant detail URL"""
    return reverse('participant:participant-detail', args=[participant_id])


class ParticipantsApiTests(TestCase):
    """Tests for participant API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@company.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_participants_for_authenticated_user(self):
        """Test retrieving participant list successfully"""

        Participant.objects.create(
            grade=sample_grade(),
            church=sample_church(),
            parent=sample_parent(),
            pickup_person=sample_pickup_person())

        Participant.objects.create(
            grade=sample_grade(),
            church=sample_church(),
            parent=sample_parent(),
            pickup_person=sample_pickup_person(),
            first_name='Aba',
            date_of_birth='2000-01-01'
        )

        participants = Participant.objects.all().order_by('id')
        res = self.client.get(PARTICIPANT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ParticipantSerializer(participants, many=True)
        self.assertEqual(serializer.data, res.data)

    def test_add_participant(self):
        """Test add new participant succesfully"""
        grade = sample_grade()
        parent = sample_parent()
        church = sample_church()
        pickup_person = sample_pickup_person

        payload = {
            'first_name': 'Aba ',
            'last_name': 'Asomaning',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': grade,
            'church': church,
            'parent': parent,
            'pickup_person': pickup_person
        }

        res = self.client.post(PARTICIPANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        participant_created = Participant.objects.filter(
            first_name='Aba', last_name='Asomaning').exists
        self.assertTrue(participant_created)

    def test_view_participant_details(self):
        """Test viewing a specific participant detail"""
        participant = sample_participant()

        url = get_detail_url(participant.id)
        res = self.client.get(url)

        serializer = ParticipantDetailSerializer(res.data)
        self.assertEqual(res.data, serializer.data)
