from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

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
            response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)

        for i in range(5):
            product = ProductFactory()
            product.users.set([self.user])
            ViewFactory(user=self.user)

        with self.assertNumQueries(2):
            response = self.client.get(self.url)
        self.assertEqual(len(response.data), 7)

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
        with self.assertNumQueries(2):
            response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)

        for i in range(5):
            self.lesson = LessonFactory()
            self.lesson.products.set([self.product_1])
            ViewFactory(lesson=self.lesson, user=self.user)

        with self.assertNumQueries(2):
            response = self.client.get(self.url)
        self.assertEqual(len(response.data), 6)

    def test_simple(self):
        # One user can acess to 2 different products
        # but we wont to see in list only lessons from 1 product

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]), 4)

        response = self.client.get("/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductsListTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("v1:products")

    def test_url(self):
        self.assertEqual(self.url, f"/v1/products/")

    def test_simple(self):
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

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_student_count(self):
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
        self.product_2.users.set([user for user in UserFactory.create_batch(4)])

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['student_count'], 1)
        self.assertEqual(response.data[1]['student_count'], 4)

    def test_lessons_count(self):
        # product 1
        product_1 = ProductFactory()
        product_1.users.set([self.user])
        lesson_1 = LessonFactory()
        lesson_1.products.set([product_1])
        ViewFactory(lesson=lesson_1, user=self.user, is_finished=True)

        # product 2
        product_2 = ProductFactory()
        product_2.users.set([self.user])
        lesson_2 = LessonFactory.create_batch(3)
        for lesson in lesson_2:
            lesson.products.set([product_2])
            ViewFactory(lesson=lesson, user=self.user, is_finished=True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['lessons_finished'], 1)
        self.assertEqual(response.data[1]['lessons_finished'], 3)

    def test_total_progress(self):
        # product 1
        product_1 = ProductFactory()
        product_1.users.set([self.user])
        lesson_1 = LessonFactory()
        lesson_1.products.set([product_1])
        lesson_2 = LessonFactory()
        lesson_2.products.set([product_1])
        ViewFactory(
            lesson=lesson_1,
            user=self.user,
            progress=75,
            is_finished=True)
        ViewFactory(
            lesson=lesson_2,
            user=self.user,
            progress=75,
            is_finished=True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['total_progress'], 150)
        self.assertEqual(response.data[0]['shopping_percentage'], 50)

    def test_num_queries(self):
        user_1 = UserFactory()
        user_2 = UserFactory()
        user_3 = UserFactory()

        # product 1
        product_1 = ProductFactory()
        product_1.users.set([user_1])
        ViewFactory(user=user_1)

        # product 2
        product_2 = ProductFactory()
        product_2.users.set([user_2])
        ViewFactory(user=user_2)

        # product 3
        product_3 = ProductFactory()
        product_3.users.set([user_3])
        ViewFactory(user=user_3)

        product_2.users.set([user for user in UserFactory.create_batch(4)])

        with self.assertNumQueries(10):
            self.client.get(self.url)

