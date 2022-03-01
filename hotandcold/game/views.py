from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .models import Player
from .forms import UserRegistrationForm, EventCreationForm


def home(request):
    return render(request, "game/home.html", None)


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")

    form = AuthenticationForm()
    return render(request, "game/temp/log_in.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            p = Player(user=user)
            p.save()
            login(request, user)
            return redirect("home")

    form = UserRegistrationForm()
    return render(request, "game/temp/register.html", {"form": form})


def game(request):
    return render(request, "game/temp/game.html", None)


def create_event(request):
    form = EventCreationForm
    return render(request, "game/temp/create_event.html", {"form": form})


def profile(request):
    return render(request, "game/profile.html")