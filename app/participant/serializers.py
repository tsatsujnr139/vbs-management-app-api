from rest_framework import serializers

from core.models import (Grade, Church,
                         Participant, Volunteer)


class GradeSerializer(serializers.ModelSerializer):
    """serializer for grade model"""

    class Meta:
        model = Grade
        fields = ('__all__')
        read_only_fields = ('id',)


class ChurchSerializer(serializers.ModelSerializer):
    """Serializer for church model"""
    class Meta:
        model = Church
        fields = ('__all__')
        read_only_fields = ('id',)


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer for participant model"""

    class Meta:
        model = Participant
        fields = ('__all__')
        read_only_fields = ('id',)


class ParticipantDetailSerializer(ParticipantSerializer):
    """Serializer for Participant Detail"""


class VolunteerSerializer(serializers.ModelSerializer):
    """Serializer for Volunteer model"""

    class Meta:
        model = Volunteer
        fields = ('__all__')
        read_only_fields = ('id',)
