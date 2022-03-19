"""URL configuration for hotandcold project.

The `urlpatterns` list routes URLs to views.

The following list shows the mapping:
    / -> See game.urls.
    /admin -> See admin.site.urls

For more information, see
https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path


# URL to view routing.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("game.urls")),
]
