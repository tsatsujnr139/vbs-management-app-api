from rest_framework import serializers

from core.models import Grade


class GradeSerializer(serializers.ModelSerializer):
    """serializer for grade model"""

    class Meta:
        model = Grade
        fields = ('id', 'name',)
        read_only_fields = ('id',)
