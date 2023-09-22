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


class LessonViewedSerializer(serializers.ModelSerializer):
    views = ViewSerializer(many=True)
    last_viewed = serializers.DateTimeField()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'views', 'last_viewed')


class ProductsSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'user_count')

    def get_user_count(self, product):
        return product.user_count()


class ProductStatSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    lesson_count = serializers.IntegerField()
    total_progress = serializers.IntegerField()
    student_count = serializers.IntegerField()
    acquisition_percentage = serializers.FloatField()
