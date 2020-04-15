from rest_framework import viewsets, mixins, pagination
from rest_framework.authentication import TokenAuthentication
from participant import permissions


from participant.serializers import (GradeSerializer,
                                     ChurchSerializer,
                                     ParticipantSerializer, VolunteerSerializer
                                     )

from core.models import (Grade, Church,
                         Participant, Volunteer)
from core.mixins import CountModelMixin


class GradeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    """view for managing grades in the application"""
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()


class ChurchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin, CountModelMixin):
    """view for managing churches in the application"""
    serializer_class = ChurchSerializer
    queryset = Church.objects.all()


class ParticipantViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                         CountModelMixin):
    serializer_class = ParticipantSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.ListAdminOnly,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        queryset = Participant.objects.all()
        grade = self.request.query_params.get('grade', None)
        if grade is not None:
            queryset = queryset.filter(grade=grade)
        return queryset


class VolunteerViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                       mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       CountModelMixin):
    serializer_class = VolunteerSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    queryset = Volunteer.objects.all()
    permission_classes = (permissions.ListAdminOnly,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')
