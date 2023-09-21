from django.urls import path

from HardCodeApp.views import UserLessonsView, UserProductsView

urlpatterns = [
    path(
        'user_lessons/<int:pk>/',
        UserLessonsView.as_view(),
        name="user_lessons", ),
    path(
        'product_lessons/<int:user>/product/<int:product>/',
        UserProductsView.as_view(),
        name="product_lessons", )
]
