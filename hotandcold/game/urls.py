from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test/", views.test, name="test"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    path("game/", views.game, name="game"),
    path("create_event/", views.create_event, name="create event"),
    path("profile/", views.profile, name="profile"),
]
