from django.utils.timezone import now
from django.db.models import Sum, Count
from rest_framework import viewsets, mixins, pagination
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
    queryset = Grade.objects.all().order_by('-id')


class ChurchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """view for managing churches in the application"""
    serializer_class = ChurchSerializer
    queryset = Church.objects.all().order_by('-id')


class ParticipantViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin):
    serializer_class = ParticipantSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        queryset = Participant.objects.all().order_by('-id')
        grade = self.request.query_params.get('grade', None)
        last_name = self.request.query_params.get('last_name', None)
        if grade is not None:
            queryset = queryset.filter(grade=grade)
        if last_name is not None:
            queryset = queryset.filter(last_name__icontains=last_name)
        return queryset


class VolunteerViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                       mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin):
    serializer_class = VolunteerSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = ('id')

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        grade = self.request.query_params.get('grade', None)
        last_name = self.request.query_params.get('last_name', None)
        queryset = Volunteer.objects.all().order_by('-id')
        if grade is not None:
            queryset = Volunteer.objects.filter(grade=grade)
        if last_name is not None:
            queryset = Volunteer.objects.filter(last_name__icontains=last_name)
        return queryset


class DashboardDataViewSet(viewsets.ViewSet):
    """
    View to return dashboard data

    * Requires token authentication
    * Only admin users are able to access this view

    """
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        """
        Return dashboard data
        """
        participant_queryset = Participant.objects.all()
        volunteer_queryset = Volunteer.objects.all()

        year, week, _ = now().isocalendar()

        participants_this_week_queryset = participant_queryset.filter(
            created__iso_year=year, created__week=week)
        volunteers_this_week_queryset = volunteer_queryset.filter(
            created__iso_year=year, created__week=week)

        participant_church_queryset = participant_queryset.distinct('church')
        volunteer_church_queryset = volunteer_queryset.distinct('church')

        participant_churches_this_week_queryset = (
            participants_this_week_queryset.distinct('church'))
        volunteer_churches_this_week_queryset = (
            volunteers_this_week_queryset.distinct('church'))

        participant_class_distribution = Participant.objects.values(
            'grade').annotate(count=Count('grade'))

        volunteer_class_distribution = Volunteer.objects.values(
            'preferred_class').annotate(count=Count('preferred_class'))

        dashboard_data = {
            'overview': {
                'participants': participant_queryset.count(),
                'volunteers': volunteer_queryset.count(),
                'participant_churches': participant_church_queryset.count(),
                'volunteer_churches': volunteer_church_queryset.count(),
                'participants_this_week':
                    participants_this_week_queryset.count(),
                'volunteers_this_week': volunteers_this_week_queryset.count(),
                'participant_churches_this_week':
                participant_churches_this_week_queryset.count(),
                'volunteer_churches_this_week':
                volunteer_churches_this_week_queryset.count(),
            },
            'distributions': {
                'participant_class_distribution':
                    participant_class_distribution,
                'volunteer_class_distribution': volunteer_class_distribution
            }
        }
        return Response(dashboard_data)
