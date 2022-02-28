from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.log_in, name="log_in"),
    path("register/", views.register, name="register"),
    path("game/", views.game, name="game"),
    path("profile/", views.profile, name="profile"),
]
