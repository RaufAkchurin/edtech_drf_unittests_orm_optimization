from django.shortcuts import render
from rest_framework import generics

from HardCodeApp.models import Lesson
from HardCodeApp.serializers import UserLessonsListSerializer


# Create your views here.

class UserLessonsView(generics.ListAPIView):
    serializer_class = UserLessonsListSerializer
    queryset = Lesson.objects.all()


    def get_queryset(self):
        user_pk = self.request.parser_context["kwargs"].get("pk", None)
        return super().get_queryset()
