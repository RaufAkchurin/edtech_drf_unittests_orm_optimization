from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import generics

from HardCodeApp.models import Lesson, View
from HardCodeApp.serializers import UserLessonsListSerializer


# Create your views here.

class UserLessonsView(generics.ListAPIView):
    serializer_class = UserLessonsListSerializer
    queryset = Lesson.objects.all()
    queryset = queryset.prefetch_related("products")

    def get_queryset(self):
        user_id = self.request.parser_context["kwargs"].get("pk", None)
        queryset = super().get_queryset().filter(views__user_id=user_id)
        if queryset.count() > 0:
            return queryset
        else:
            return super().get_queryset()
