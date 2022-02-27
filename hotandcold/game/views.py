from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render


def home(request):
    return render(request, "game/homeScreen.html", None)


def login(request):
    return render(request, "game/loginScreen.html", None)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")

    form = UserCreationForm()
    return render(request, "game/accountCreation.html", {"form": form})


def game(request):
    return render(request, "game/gameScreen.html", None)


def profile(request):
    return HttpResponse("User profile page.")
