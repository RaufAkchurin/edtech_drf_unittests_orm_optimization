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


class LessonViewedSerializer(serializers.ModelSerializer):
    views = ViewSerializer(many=True)
    last_viewed = serializers.DateTimeField()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'views', 'last_viewed')


class ProductStatSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    lessons_finished = serializers.IntegerField()
    total_progress = serializers.IntegerField()
    student_count = serializers.IntegerField()
    shopping_percentage = serializers.FloatField()
