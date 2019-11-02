from rest_framework import serializers

from core.models import Grade, Church, PickupPerson, Parent


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
