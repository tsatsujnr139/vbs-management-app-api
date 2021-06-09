from rest_framework import serializers

from core.models import (
    Grade,
    Church,
    Participant,
    Volunteer,
    AttendanceType,
    Session,
)


class GradeSerializer(serializers.ModelSerializer):
    """serializer for grade model"""

    class Meta:
        model = Grade
        fields = "__all__"
        read_only_fields = ("id",)


class AttendanceTypeSerializer(serializers.ModelSerializer):
    """serializer for session model"""

    class Meta:
        model = AttendanceType
        fields = "__all__"
        read_only_fields = ("id",)


class SessionSerializer(serializers.ModelSerializer):
    """serializer for session model"""

    eligible_grades = GradeSerializer(many=True, read_only=True)
    supported_attendance_types = AttendanceTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = "__all__"
        read_only_fields = ("id",)


class ChurchSerializer(serializers.ModelSerializer):
    """Serializer for church model"""

    class Meta:
        model = Church
        fields = "__all__"
        read_only_fields = ("id",)


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer for participant model"""

    pickup_person_name = serializers.CharField(required=False)
    pickup_person_contact_no = serializers.CharField(required=False)
    medical_info = serializers.CharField(required=False)

    class Meta:
        model = Participant
        fields = "__all__"
        read_only_fields = ("id",)


class ParticipantDetailSerializer(ParticipantSerializer):
    """Serializer for Participant Detail"""


class VolunteerSerializer(serializers.ModelSerializer):
    """Serializer for Volunteer model"""

    class Meta:
        model = Volunteer
        fields = "__all__"
        read_only_fields = ("id",)
