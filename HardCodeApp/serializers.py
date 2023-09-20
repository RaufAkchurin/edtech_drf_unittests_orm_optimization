from rest_framework import serializers

from HardCodeApp.models import Lesson


class UserLessonsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
