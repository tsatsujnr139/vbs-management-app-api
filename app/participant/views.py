from rest_framework import viewsets, mixins
from participant import permissions

from participant.serializers import (GradeSerializer, ChurchSerializer,
                                     PickupPersonSerializer, ParentSerializer)

from core.models import Grade, Church, PickupPerson, Parent


class GradeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    """view for managing grades in the application"""
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()


class ChurchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """view for managing churches in the application"""
    serializer_class = ChurchSerializer
    queryset = Church.objects.all()


class PickupPersonViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    """View for managing pickup persons for participants"""
    serializer_class = PickupPersonSerializer
    queryset = PickupPerson.objects.all()


class ParentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """View for managing parents of participants"""
    serializer_class = ParentSerializer
    queryset = Parent.objects.all()
    permission_classes = (permissions.ListAdminOnly,)
