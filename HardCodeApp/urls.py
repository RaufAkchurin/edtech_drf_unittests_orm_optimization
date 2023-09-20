from django.urls import path

from HardCodeApp.views import UserLessonsView

urlpatterns = [
    path(
        'user_lessons/<int:pk>/',
        UserLessonsView.as_view(),
        name="user_lessons", )
]
