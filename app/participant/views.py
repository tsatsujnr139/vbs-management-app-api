from rest_framework import viewsets, mixins, pagination
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
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
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        queryset = Participant.objects.all()
        grade = self.request.query_params.get('grade', None)
        last_name = self.request.query_params.get('last_name', None)
        if grade is not None:
            queryset = queryset.filter(grade=grade)
        if last_name is not None:
            queryset = queryset.filter(last_name__icontains=last_name)
        return queryset


class VolunteerViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                       mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       CountModelMixin):
    serializer_class = VolunteerSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        grade = self.request.query_params.get('grade', None)
        last_name = self.request.query_params.get('last_name', None)
        queryset = Volunteer.objects.all()
        if grade is not None:
            queryset = Volunteer.objects.filter(grade=grade)
        if last_name is not None:
            queryset = Volunteer.objects.filter(last_name__icontains=last_name)
        return queryset


class DashboardDataViewSet(viewsets.GenericViewSet):
    """
    View to return dashboard data

    * Requires token authentication
    * Only admin users are able to access this view

    """
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)

    @action(methods="[GET]", detail=False, url_path="data",)
    def get(self, request, *args, **kwargs):
        """
        Return dashboard data
        """
        participant_queryset = Participant.objects.all()
        volunteer_queryset = Volunteer.objects.all()
        participant_church_queryset = participant_queryset.distinct('church')
        volunteer_church_queryset = volunteer_queryset.distinct('church')
        dashboard_data = {
            'participant_count': participant_queryset.count(),
            'volunteer_count': volunteer_queryset.count(),
            'participant_church_count': participant_church_queryset.count(),
            'volunteer_church_count': volunteer_church_queryset.count()
        }
        return Response(dashboard_data)
