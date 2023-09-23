import random

import factory
from django.contrib.auth import get_user_model
from factory import SubFactory, Faker
from factory.django import DjangoModelFactory

from HardCodeApp.models import Product, Lesson, View


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user {n}")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("word")
    owner = SubFactory(UserFactory)


class LessonFactory(DjangoModelFactory):
    class Meta:
        model = Lesson

    name = Faker("word")
    duration = random.randint(10, 10 ** 2)


class ViewFactory(DjangoModelFactory):
    class Meta:
        model = View

    lesson = SubFactory(LessonFactory)
    user = SubFactory(UserFactory)
    progress = random.randint(10, 10 ** 2)
