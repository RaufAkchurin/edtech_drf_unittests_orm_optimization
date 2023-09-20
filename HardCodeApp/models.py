from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=10)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
    )


class Access(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="accesses",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accesses",
    )


class Lesson(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    name = models.CharField(max_length=10)
    link = models.URLField()
    duration = models.IntegerField()


class View(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="views",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="views",
    )
    finished = models.BooleanField()
