from django.urls import path

from HardCodeApp.views import LessonsByUserView, LessonsByProductUserView, ProductStatAPIView

urlpatterns = [
    path(
        'user_lessons/<int:pk>/',
        LessonsByUserView.as_view(),
        name="user_lessons", ),
    path(
        'product_lessons/<int:user>/product/<int:product>/',
        LessonsByProductUserView.as_view(),
        name="product_lessons", ),
    path(
        'products/',
        ProductStatAPIView.as_view(),
        name="products", ),
]
