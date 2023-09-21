from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from HardCodeApp.models import Lesson, View, Product
from HardCodeApp.serializers import LessonSerializer


# Create your views here.

class LessonsByUserView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    queryset = queryset.prefetch_related("products")

    def get_queryset(self):
        user_id = self.request.parser_context["kwargs"].get("pk", None)
        queryset = super().get_queryset().filter(views__user_id=user_id)
        if queryset.count() > 0:
            return queryset
        else:
            return super().get_queryset()


class LessonsByProductUserView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        user_id = self.request.parser_context["kwargs"].get("user", None)
        product_id = self.request.parser_context["kwargs"].get("product", None)
        queryset = super().get_queryset().filter(products__in=[product_id])
        return queryset


