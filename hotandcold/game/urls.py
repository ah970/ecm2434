"URL configuration for game app.

The `urlpatterns` list routes URLs to views.

The following list shows the mapping:
    / -> Home.
    /test/ -> Test.
    /login/ -> Login.
    /logout/ -> Logout.
    /register/ -> Account creation/registration.
    /game/ -> Game.
    /create_event -> Event creation.
    /profile/ -> User profile.
"""

from django.urls import path

from . import views


# URL to view routing.
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
