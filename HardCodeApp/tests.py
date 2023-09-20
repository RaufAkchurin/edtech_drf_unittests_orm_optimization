from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from HardCodeApp.models import Product, Lesson


# Create your tests here.

class AnimalListTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username="owner")
        self.user = User.objects.create(username="first")
        self.url = reverse("v1:user_lessons", args=[self.user.id])
        # prepare data without Factories

        # product
        self.product = Product.objects.create(
            owner=self.owner,
        )
        self.product.users.set([self.user])
        # lessons
        self.lesson_1 = Lesson.objects.create(
            name="lesson_first",
            duration=1,
        )
        self.lesson_2 = Lesson.objects.create(
            name="lesson_second",
            duration=2,
        )


    def test_url(self):
        self.assertEqual(self.url, f"/v1/user_lessons/{self.user.id}/")

    def test_simple(self):
        with self.assertNumQueries(3):
            response =self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(response.data[0]), 5)
