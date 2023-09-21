
from rest_framework import generics

from HardCodeApp.models import Lesson
from HardCodeApp.serializers import LessonSerializer, LessonSerializerViewed


# Create your views here.

class LessonsByUserView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    queryset = queryset.prefetch_related("views")

    def get_queryset(self):
        user_id = self.request.parser_context["kwargs"].get("pk", None)
        queryset = super().get_queryset().filter(views__user_id=user_id)
        return queryset


class LessonsByProductUserView(generics.ListAPIView):
    serializer_class = LessonSerializerViewed
    queryset = Lesson.objects.all().prefetch_related("views")

    def get_queryset(self):
        user_id = self.request.parser_context["kwargs"].get("user", None)
        product_id = self.request.parser_context["kwargs"].get("product", None)
        queryset = self.queryset.filter(products__id=product_id,  views__user_id=user_id)
        return queryset


