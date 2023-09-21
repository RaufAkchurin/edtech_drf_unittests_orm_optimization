import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
import time

from HardCodeApp.factory import UserFactory, ProductFactory, LessonFactory, ViewFactory


class ViewModelTestCase(APITestCase):
    def test_is_finished_zero_division(self):
        lesson = LessonFactory(duration=0)
        view = ViewFactory(lesson=lesson, progress=0)
        self.assertEqual(view.is_finished, False)

    def test_is_finished_changes(self):
        lesson = LessonFactory(duration=100)
        view = ViewFactory(lesson=lesson, progress=50)
        self.assertEqual(view.is_finished, False)

        view.progress = 85
        view.save()
        view.refresh_from_db()
        self.assertEqual(view.is_finished, True)


class LessonsByUserListTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="first")
        self.url = reverse("v1:user_lessons", args=[self.user.id])
        # user 1
        self.product_1 = ProductFactory()
        self.product_1.users.set([self.user])
        ViewFactory(user=self.user)

        # user 1
        self.product_2 = ProductFactory()
        self.product_2.users.set([self.user])
        ViewFactory(user=self.user)

        # user 2
        self.user_2 = UserFactory(username='second')
        self.product_2 = ProductFactory()
        self.product_2.users.set([self.user_2])
        ViewFactory(user=self.user_2)

    def test_url(self):
        self.assertEqual(self.url, f"/v1/user_lessons/{self.user.id}/")

    def test_without_pk(self):
        url = "/v1/user_lessons/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_num_queries(self):
        with self.assertNumQueries(2):
            self.client.get(self.url)

    def test_simple_user_1(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(len(response.data[0]), 3)

    def test_simple_user_2(self):
        response = self.client.get(f"/v1/user_lessons/{self.user_2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]), 3)


class LessonsByProductListTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username="owner")
        self.user = UserFactory()

        # product 1
        self.product_1 = ProductFactory()
        self.product_1.users.set([self.user])
        self.lesson_1 = LessonFactory()
        self.lesson_1.products.set([self.product_1])
        self.view_1 = ViewFactory(lesson=self.lesson_1, user=self.user)

        # product 2
        self.product_2 = ProductFactory()
        self.product_2.users.set([self.user])
        self.lesson_2 = LessonFactory()
        self.lesson_2.products.set([self.product_2])
        self.view_2 = ViewFactory(lesson=self.lesson_2, user=self.user)

        self.url = reverse("v1:product_lessons", args=[self.user.id, self.product_1.id])

    def test_url(self):
        self.assertEqual(self.url, f"/v1/product_lessons/{self.user.id}/product/{self.product_1.id}/")

    def test_num_queries(self):
        with self.assertNumQueries(3):
            self.client.get(self.url)

    def test_simple(self):
        # Один юзер имеет доступ к двум разным продуктам, и мы хотим в списке увидеть только уроки
        # от 1 продукта
        # TODO optimize queries
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]), 4)

        # assert last_viewed field
        self.assertEqual(response.data[0]['last_viewed'], self.view_1.last_viewed)
        self.assertNotEqual(response.data[0]['last_viewed'], self.view_2.last_viewed)

        response = self.client.get("/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductsListTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(username="owner")
        self.user = UserFactory()

        # product 1
        self.product_1 = ProductFactory()
        self.product_1.users.set([self.user])
        self.lesson_1 = LessonFactory()
        self.lesson_1.products.set([self.product_1])
        self.view_1 = ViewFactory(lesson=self.lesson_1, user=self.user)

        # product 2
        self.product_2 = ProductFactory()
        self.product_2.users.set([self.user])
        self.lesson_2 = LessonFactory()
        self.lesson_2.products.set([self.product_2])
        self.view_2 = ViewFactory(lesson=self.lesson_2, user=self.user)

        self.url = reverse("v1:products")

    def test_url(self):
        self.assertEqual(self.url, f"/v1/products/")

    def test_num_queries(self):
        with self.assertNumQueries(3):
            self.client.get(self.url)

    def test_simple(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
