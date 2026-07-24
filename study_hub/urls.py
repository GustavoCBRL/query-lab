from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/",include("django.contrib.auth.urls")),
    path("register", views.register, name="register"),
    path("topics/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("topics/<int:topic_id>/practices/", views.practice_list, name="practice_list"),
    path("submit-answer/<int:question_id>/", views.submit_answer, name="answer"),
    path("dashboard", views.dashboard, name="dashboard" ),
    path("practice/<int:practice_id>/", views.practice_exercise, name="practice"),
    path("lab/", views.practice_list, name="lab")
]