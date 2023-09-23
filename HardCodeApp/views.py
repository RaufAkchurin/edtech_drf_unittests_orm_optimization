from django.contrib.auth.models import User
from django.db.models import Max, Sum
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
        products = Product.objects.select_related('owner').prefetch_related('users', 'users__views')

        product_stats = []
        total_user_count = User.objects.count()

        for product in products:
            lessons = Lesson.objects.filter(products=product, views__is_finished=True)
            views = View.objects.filter(lesson__in=lessons)

            # Calculate total progress and lessons finished
            total_progress = views.aggregate(total_sum=Sum('progress'))['total_sum']
            lessons_finished = lessons.count()

            # Calculate shopping percentage
            student_count = product.users.count()
            shopping_percentage = (student_count / total_user_count) * 100 if total_user_count > 0 else 0

            product_stat_data = {
                'product_id': product.id,
                'product_name': product.name,
                'lessons_finished': lessons_finished,
                'total_progress': total_progress,
                'student_count': student_count,
                'shopping_percentage': shopping_percentage
            }

            product_stats.append(product_stat_data)

        serializer = ProductStatSerializer(product_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

