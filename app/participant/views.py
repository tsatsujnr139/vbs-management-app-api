from django.urls import path

from rest_framework import viewsets, mixins, status

from participant.serializers import GradeSerializer

from core.models import Grade


class GradeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    """view for managing grades in the database"""

    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
