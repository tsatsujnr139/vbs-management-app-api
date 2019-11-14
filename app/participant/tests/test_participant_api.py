from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Participant, Grade,
                         Church, PickupPerson,
                         Parent)
from participant.serializers import ParticipantSerializer


PARTICIPANT_URL = reverse('participant:participant-list')
PARTICIPANT_COUNT_URL = reverse('participant:participant-count')


def sample_parent(**params):

    defaults = {
        'full_name': 'Aforo Asomaning',
        'primary_contact_no': '0244123456',
        'alternate_contact_no': '0255123456'
    }

    defaults.update(params)

    return Parent.objects.create(
        **defaults
    )


def sample_pickup_person(full_name='Aforo',
                         contact_no='0244123456'):
    return PickupPerson.objects.create(
        full_name=full_name,
        contact_no=contact_no
    )


def sample_church(name='Legon Interdenominational Church'):
    return Church.objects.create(
        name=name
    )


def sample_grade(name='Class 1'):
    return Grade.objects.create(
        name=name
    )


def sample_participant(grade, church, pickup_person, parent, **params):

    defaults = {
        'first_name': 'Adoma',
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
            grade=sample_grade(name='Class 2'),
            church=sample_church(name='Ridge Church'),
            parent=sample_parent(full_name='Kofi Asomaning'),
            pickup_person=sample_pickup_person()
        )

        Participant.objects.create(
            grade=sample_grade(),
            church=sample_church(),
            parent=sample_parent(),
            pickup_person=sample_pickup_person(),
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
        grade = sample_grade()
        parent = sample_parent()
        church = sample_church()
        pickup_person = sample_pickup_person()

        payload = {
            'first_name': 'Aba ',
            'last_name': 'Asomaning',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': grade.id,
            'church': church.id,
            'parent': parent.id,
            'pickup_person': pickup_person.id
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

        grade = sample_grade()
        parent = sample_parent()
        church = sample_church()
        pickup_person = sample_pickup_person()

        participant = sample_participant(
            grade=grade, parent=parent,
            church=church, pickup_person=pickup_person
        )

        url = get_detail_url(participant.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], participant.first_name)

    def test_view_participant_details_for_unauthorized_user(self):
        """
        Test viewing a specific participant detail for unauthorized user fails

        """
        grade = sample_grade()
        parent = sample_parent()
        church = sample_church()
        pickup_person = sample_pickup_person()

        participant = sample_participant(
            grade=grade, parent=parent,
            church=church, pickup_person=pickup_person
        )

        url = get_detail_url(participant.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_participant_count(self):
        """Test retrieval of number of registered participant"""
        sample_participant(
            grade=sample_grade(),
            parent=sample_parent(),
            church=sample_church(),
            pickup_person=sample_pickup_person()
        )

        sample_participant(
            grade=sample_grade(name='Class 2'),
            parent=sample_parent(full_name='Kofi Asomaning'),
            church=sample_church(name='Anglican Church'),
            pickup_person=sample_pickup_person(full_name='Sam Yeboah')
        )

        res = self.client.get(PARTICIPANT_COUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_retrieve_participant_list_by_class(self):
        """Test retrieving participant list by class api"""

        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

        grade = sample_grade()
        grade2 = sample_grade(name='Class 6')
        parent = sample_parent()
        church = sample_church()
        pickup_person = sample_pickup_person()

        payload1 = {
            'first_name': 'Ewurabena',
            'last_name': 'Surname',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': grade.id,
            'church': church.id,
            'parent': parent.id,
            'pickup_person': pickup_person.id
        }

        payload2 = {
            'first_name': 'Aba',
            'last_name': 'Asomaning',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': grade2.id,
            'church': church.id,
            'parent': parent.id,
            'pickup_person': pickup_person.id
        }

        payload3 = {
            'first_name': 'Owusua',
            'last_name': 'Yeboah',
            'gender': 'Female',
            'date_of_birth': '2000-01-01',
            'medical_information': '',
            'grade': grade.id,
            'church': church.id,
            'parent': parent.id,
            'pickup_person': pickup_person.id
        }

        self.client.post(PARTICIPANT_URL, payload1)
        self.client.post(PARTICIPANT_URL, payload2)
        self.client.post(PARTICIPANT_URL, payload3)

        res = self.client.get(PARTICIPANT_URL, {'grade': grade.id})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['first_name'], payload3['first_name'])
