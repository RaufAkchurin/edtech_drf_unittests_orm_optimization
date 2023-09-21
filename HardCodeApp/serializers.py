from rest_framework import serializers

from HardCodeApp.models import Lesson, View


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ('progress', 'is_finished')


class LessonSerializer(serializers.ModelSerializer):
    views = ViewSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'views')
