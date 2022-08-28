import random
from datetime import date, timezone

from django.conf import settings
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import mixins, pagination, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from core.constants import EVENT_DAY_TO_DATE_MAPPING
from core.messaging import send_attendance_message, send_pickup_message
from core.models import (
    AttendanceType,
    Church,
    Grade,
    Participant,
    ParticipantAttendance,
    ParticipantPickup,
    PickupCode,
    Session,
    Volunteer,
)
from participant import permissions
from participant.serializers import (
    AttendanceTypeSerializer,
    ChurchSerializer,
    GradeSerializer,
    ParticipantSerializer,
    SessionSerializer,
    VolunteerSerializer,
)


class GradeViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """view for managing grades in the application"""

    serializer_class = GradeSerializer
    queryset = Grade.objects.all().order_by("-id")


class AttendanceTypeViewSet(viewsets.ModelViewSet):
    """view for managing attendance types in the application"""

    serializer_class = AttendanceTypeSerializer
    queryset = AttendanceType.objects.all().order_by("-id")


class SessionViewSet(viewsets.ModelViewSet):
    """view for managing event session option in the application"""

    serializer_class = SessionSerializer
    queryset = Session.objects.all().order_by("-id")


class ChurchViewSet(viewsets.ModelViewSet):
    """view for managing churches in the application"""

    serializer_class = ChurchSerializer
    queryset = Church.objects.all().order_by("-id")


class ParticipantViewset(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = "id"

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        queryset = (
            Participant.objects.all()
            .order_by("-id")
            .select_related(
                "grade", "participantattendance", "participantpickup", "pickupcode"
            )
        )
        grade = self.request.query_params.get("grade", None)
        q = self.request.query_params.get("q", None)
        if grade:
            queryset = queryset.filter(grade__name=grade)
        if q:
            today = date.today()
            today_str = f"{today:%d-%m-%Y}"
            today_event = EVENT_DAY_TO_DATE_MAPPING[today_str]
            day_pickup_code = f"pickupcode__{today_event}"
            queryset = queryset.filter(
                Q(last_name__icontains=q)
                | Q(first_name__icontains=q)
                | Q(**{day_pickup_code: q})
            )

        return queryset

    @action(detail=True, methods=["post"])
    def admit(self, request, pk=None, id=None):
        today = date.today()
        today_str = f"{today:%d-%m-%Y}"
        if f"{today_str}" not in settings.EVENT_DATES:
            return JsonResponse(
                {
                    "detail": "You can only record attendance on a valid VBS date for this year"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Get day mapping for date
        today_event = EVENT_DAY_TO_DATE_MAPPING[today_str]
        day_filter_is_null = f"{today_event}__isnull"
        if ParticipantAttendance.objects.filter(
            participant=self.get_object(), **{day_filter_is_null: False}
        ):
            return JsonResponse(
                {
                    "detail": "This participant has already been marked as present for today."
                },
                status=200,
            )
        ParticipantAttendance.objects.update_or_create(
            participant=self.get_object(), defaults={**{today_event: timezone.now()}}
        )
        # Create participant pickup code record
        pickup_code = random.randint(10000, 99999)
        PickupCode.objects.update_or_create(
            participant=self.get_object(), defaults={**{today_event: pickup_code}}
        )

        send_attendance_message(
            participant=self.get_object(), vbs_day=today_event, pickup_code=pickup_code
        )
        return JsonResponse(
            {"detail": "Attendance recorded successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def pickup(self, request, pk=None, id=None):
        today = date.today()
        today_str = f"{today:%d-%m-%Y}"
        if f"{today_str}" not in settings.EVENT_DATES:
            return JsonResponse(
                {
                    "detail": "You can only record pickup on a valid VBS date for this year"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.data.get("pickup_person"):
            return JsonResponse(
                {"detail": "Please enter the pickup person's name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Get day mapping for date
        today_event = EVENT_DAY_TO_DATE_MAPPING[today_str]
        day_filter_is_null = f"{today_event}__isnull"
        if ParticipantPickup.objects.filter(
            participant=self.get_object(), **{day_filter_is_null: False}
        ):
            return JsonResponse(
                {
                    "detail": "This participant has already been marked as picked up for today."
                },
                status=202,
            )

        day_pickup_person = f"{today_event}_pickup_person"
        ParticipantPickup.objects.update_or_create(
            participant=self.get_object(),
            defaults={
                **{
                    day_pickup_person: request.data.get("pickup_person"),
                    today_event: timezone.now(),
                }
            },
        )
        send_pickup_message(
            participant=self.get_object(),
            vbs_day=today_event,
            pickup_person=request.data.get("pickup_person"),
        )
        return JsonResponse(
            {"detail": "Pickup recorded successfully"}, status=status.HTTP_200_OK
        )


class VolunteerViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerSerializer
    pagination_class = pagination.api_settings.DEFAULT_PAGINATION_CLASS
    permission_classes = (permissions.isAdminUser,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = "id"

    def get_queryset(self):
        """retrieve participants list for authenticated user"""
        grade = self.request.query_params.get("grade", None)
        last_name = self.request.query_params.get("last_name", None)
        queryset = Volunteer.objects.all().order_by("-id")
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

        year, week, _ = timezone.now().isocalendar()

        participants_this_week_queryset = participant_queryset.filter(
            created__iso_year=year, created__week=week
        )
        volunteers_this_week_queryset = volunteer_queryset.filter(
            created__iso_year=year, created__week=week
        )

        participant_church_queryset = participant_queryset.distinct("church")
        volunteer_church_queryset = volunteer_queryset.distinct("church")

        participant_churches_this_week_queryset = (
            participants_this_week_queryset.distinct("church")
        )
        volunteer_churches_this_week_queryset = (
            volunteers_this_week_queryset.distinct("church")
        )

        participant_class_distribution = Participant.objects.values(
            "grade"
        ).annotate(count=Count("grade"))

        volunteer_class_distribution = Volunteer.objects.values(
            "preferred_class"
        ).annotate(count=Count("preferred_class"))

        dashboard_data = {
            "overview": {
                "participants": participant_queryset.count(),
                "volunteers": volunteer_queryset.count(),
                "participant_churches": participant_church_queryset.count(),
                "volunteer_churches": volunteer_church_queryset.count(),
                "participants_this_week": participants_this_week_queryset.count(),
                "volunteers_this_week": volunteers_this_week_queryset.count(),
                "participant_churches_this_week": participant_churches_this_week_queryset.count(),
                "volunteer_churches_this_week": volunteer_churches_this_week_queryset.count(),
            },
            "distributions": {
                "participant_class_distribution": participant_class_distribution,
                "volunteer_class_distribution": volunteer_class_distribution,
            },
        }
        return Response(dashboard_data)
