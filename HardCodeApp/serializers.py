from rest_framework import serializers

from HardCodeApp.models import Lesson, View, Product


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ('progress', 'is_finished')


class LessonSerializer(serializers.ModelSerializer):
    views = ViewSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'views')


class LessonSerializerViewed(serializers.ModelSerializer):
    views = ViewSerializer(many=True)
    last_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'views', 'last_viewed')

    def get_last_viewed(self, obj):
        last_viewed = View.objects.filter(lesson=obj).values('last_viewed')[:1]
        if last_viewed:
            return last_viewed[0]['last_viewed']
        else:
            return None
