from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UserCreationForm


def home(request):
    return render(request, "game/homeScreen.html", None)


def log_in(request):
    return render(request, "game/loginScreen.html", None)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    form = UserCreationForm()
    return render(request, "game/accountCreation.html", {"form": form})


def game(request):
    return render(request, "game/gameScreen.html", None)


def profile(request):
    return render(request, "game/userProfile.html")
