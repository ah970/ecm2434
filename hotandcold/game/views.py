from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "game/homeScreen.html", None)


def login(request):
    return render(request, "game/loginScreen.html", None)


def register(request):
    return render(request, "game/accountCreation.html", None)


def game(request):
    return render(request, "game/gameScreen.html", None)


def profile(request):
    return HttpResponse("User profile page.")
