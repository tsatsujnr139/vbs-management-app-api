from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from participant import permissions

from participant.serializers import (GradeSerializer,
                                     ChurchSerializer,
                                     PickupPersonSerializer, ParentSerializer,
                                     ParticipantSerializer, VolunteerSerializer
                                     )

from core.models import (Grade, Church, PickupPerson,
                         Parent, Participant, Volunteer)


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
    permission_classes = (permissions.ListAdminOnly,)
    authentication_classes = (TokenAuthentication,)


class ParentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """View for managing parents of participants"""
    serializer_class = ParentSerializer
    queryset = Parent.objects.all()
    permission_classes = (permissions.ListAdminOnly,)
    authentication_classes = (TokenAuthentication,)


class ParticipantViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    permission_classes = (permissions.ListAdminOnly,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')


class VolunteerViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                       mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = VolunteerSerializer
    queryset = Volunteer.objects.all()
    permission_classes = (permissions.ListAdminOnly,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')
