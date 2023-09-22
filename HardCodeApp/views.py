from django.contrib.auth.models import User
from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from HardCodeApp.models import Lesson, Product, View
from HardCodeApp.serializers import LessonSerializer, LessonViewedSerializer, ProductStatSerializer


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


class ProductStatAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()

        product_stats = []
        for product in products:
            # lessons
            lessons = Lesson.objects.filter(products=product, views__is_finished=True).distinct()
            total_lessons = lessons.count()

            # views for total_progress
            views = View.objects.filter(lesson__in=lessons)
            total_progress = views.aggregate(total_sum=Sum('progress'))['total_sum']

            student_count = product.users.count()
            acquisition_percentage = (student_count / User.objects.count()) * 100 if User.objects.count() > 0 else 0

            product_stat_data = {
                'product_id': product.id,
                'product_name': product.name,
                'lesson_count': total_lessons,  # lessons_finished
                'total_progress': total_progress,
                'student_count': student_count,
                'acquisition_percentage': acquisition_percentage
            }

            product_stats.append(product_stat_data)

        serializer = ProductStatSerializer(product_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
