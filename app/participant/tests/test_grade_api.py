from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Grade
from participant.serializers import GradeSerializer

GRADE_URL = reverse('participant:grade-list')


class GradeApiTests(TestCase):
    """test grade api's"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_grades_successfully(self):
        """test grades are retrieved successfully"""

        Grade.objects.create(name='Class 1')
        Grade.objects.create(name='Class 2')

        grades = Grade.objects.all().order_by('id')
        serializer = GradeSerializer(grades, many=True)
        res = self.client.get(GRADE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_add_grade(self):
        """test adding a new grade"""
        payload = {
            'name': 'Class 1'
        }

        res = self.client.post(GRADE_URL, payload)
        grade_exists = Grade.objects.filter(name=payload['name']).exists
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(grade_exists)

    def test_add_grade_invalid_payload(self):
        """test grade with invalid payload fails"""

        res = self.client.post(GRADE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
