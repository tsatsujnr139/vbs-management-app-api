from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='user@email.com', password='samplepassword'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_parent(full_name='Aforo', primary_contact_no='0244123456',
                  alternate_contact_no='0255123456'):
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


class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """test creating a new user with an email is  successful"""
        email = 'user@email.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@CLUTCHCODE.COM'
        user = get_user_model().objects.create_user(email, 'password')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password')

    def test_create_new_superuser_is_successful(self):
        """test creating a new supseruser is successful"""
        email = 'test@clutchcode.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_grade_str(self):
        """test grade string representation"""
        grade = models.Grade.objects.create(
            name='Class 1',
        )

        self.assertEqual(str(grade), grade.name)

    def test_church_str(self):
        """test string representation of church model"""
        church = models.Church.objects.create(
            name='Legon Interdenominational Church'
        )

        self.assertEqual(str(church), church.name)

    def test_pickup_person_str(self):
        """test pickup person string representation"""
        pickup_person = models.PickupPerson.objects.create(
            full_name="Aforo Asomaning", contact_no="0244123456")
        self.assertEqual(str(pickup_person), pickup_person.full_name)

    def test_parent_str(self):
        """Test string representation of parent model"""
        parent = models.Parent.objects.create(
            full_name="Aforo Asomaning",
            primary_contact_no='0244123456',
            alternate_contact_no='0559412168',
            email='user@email.com'
        )

        self.assertEqual(str(parent), parent.full_name)

    def test_participant_str(self):
        """test particpant string representation"""
        participant = models.Participant.objects.create(
            first_name='Adoma',
            last_name='Asomaning',
            grade=sample_grade(),
            church=sample_church(),
            parent=sample_parent(),
            pickup_person=sample_pickup_person(),
            gender='Male',
            date_of_birth='2000-01-01',
            medical_info='Allergic to Pineapple'

        )

        self.assertEqual(str(participant),
                         participant.first_name + " " + participant.last_name)

    def test_volunteer_str(self):
        """Test volunteer String representation"""
        volunteer = models.Volunteer.objects.create(
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

        self.assertEqual(
            str(volunteer), f'{volunteer.first_name} {volunteer.last_name}')
