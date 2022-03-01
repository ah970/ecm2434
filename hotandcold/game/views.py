from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UserCreationForm


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
                print("yes")
                login(request, user)
                print("yes")
                return redirect("home")
            else:
                print("no")

    form = AuthenticationForm()
    return render(request, "game/loginScreen.html", {"form": form})


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
