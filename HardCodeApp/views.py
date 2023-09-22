from django.db.models import Max
from rest_framework import generics
from HardCodeApp.models import Lesson, Product
from HardCodeApp.serializers import LessonSerializer, LessonViewedSerializer, ProductsSerializer

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
    serializer_class = LessonViewedSerializer
    queryset = Lesson.objects.all()
    queryset = queryset.prefetch_related("views")

    def get_queryset(self):
        user_id = self.request.parser_context["kwargs"].get("user", None)
        product_id = self.request.parser_context["kwargs"].get("product", None)
        queryset = super().get_queryset().filter(products__id=product_id, views__user_id=user_id)
        queryset = queryset.annotate(last_viewed=Max('views__last_viewed'))
        return queryset


class ProductsView(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()

    def get_queryset(self):

        return super().get_queryset()



