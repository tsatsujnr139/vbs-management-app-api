from rest_framework import serializers

from core.models import (Grade, Church, PickupPerson,
                         Parent, Participant, Volunteer)


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


class PickupPersonSerializer(serializers.ModelSerializer):
    """ Serializer for pickup person model"""

    class Meta:
        model = PickupPerson
        fields = ('__all__')
        read_only_fields = ('id',)


class ParentSerializer(serializers.ModelSerializer):
    """Serializer for parent model"""

    class Meta:
        model = Parent
        fields = ('__all__')


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer for participant model"""

    parent = serializers.PrimaryKeyRelatedField(
        queryset=Parent.objects.all()
    )

    pickup_person = serializers.PrimaryKeyRelatedField(
        queryset=PickupPerson.objects.all()
    )

    church = serializers.PrimaryKeyRelatedField(
        queryset=Church.objects.all()
    )

    grade = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all()
    )

    class Meta:
        model = Participant
        fields = ('__all__')
        read_only_fields = ('id',)


class ParticipantDetailSerializer(ParticipantSerializer):
    """Serializer for Participant Detail"""
    parent = ParentSerializer(read_only=True)
    church = ChurchSerializer(read_only=True)
    pickup_person = PickupPersonSerializer(read_only=True)
    grade = GradeSerializer(read_only=True)


class VolunteerSerializer(serializers.ModelSerializer):
    """Serializer for Volunteer model"""
    church = serializers.PrimaryKeyRelatedField(
        queryset=Church.objects.all()
    )

    class Meta:
        model = Volunteer
        fields = ('__all__')
        read_only_fields = ('id',)
