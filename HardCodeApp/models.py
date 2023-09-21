from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=10)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_products",
    )
    users = models.ManyToManyField(
        User,
        related_name="users_products",
    )

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    products = models.ManyToManyField(
        Product,
        related_name="lessons",
    )
    name = models.CharField(max_length=10)
    link = models.URLField()
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


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
    progress = models.IntegerField()
    is_finished = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.progress:
            if self.progress > 15:  # its temporary version
                self.is_finished = True
        super().save(force_insert, force_update, using, update_fields)


