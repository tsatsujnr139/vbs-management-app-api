from rest_framework import serializers

from core.models import Grade, Church, PickupPerson


class GradeSerializer(serializers.ModelSerializer):
    """serializer for grade model"""

    class Meta:
        model = Grade
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class ChurchSerializer(serializers.ModelSerializer):
    """Serializer for church model"""
    class Meta:
        model = Church
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PickupPersonSerializer(serializers.ModelSerializer):
    """ Serializer for pickup person model"""

    class Meta:
        model = PickupPerson
        fields = ('__all__')
        read_only_fields = ('id',)
