from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from random import choice

from .models import Event, Player
from .forms import UserRegistrationForm, EventCreationForm


def test(request):
    return render(request, "game/extended.html", {"title": "Extended Page"})


def home(request):
    player_score_list = Player.objects.order_by("-points")[:10]
    context = {"player_score_list": player_score_list}
    return render(request, "game/home.html", context)


def log_in(request):
    title = "Login"
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
    return render(request, "game/login.html", {"form": form, "title": title})


def log_out(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            player = Player(user=user)
            player.save()
            login(request, user)
            return redirect("home")

    form = UserRegistrationForm()
    return render(request, "game/accountCreation.html", {"form": form})


def game(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            current_user = request.user
            score = int(request.POST["score"])
            current_player = Player.objects.get(user=current_user)
            current_player.points += score
            current_player.save()

            return redirect("profile")

    event_list = Event.objects.all()
    event = choice(event_list)

    return render(request, "game/game.html", {"event": event})


def create_event(request):
    if request.method == "POST":
        form = EventCreationForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            start = form.cleaned_data.get("start")
            end = form.cleaned_data.get("end")
            latitude = form.cleaned_data.get("latitude")
            longitude = form.cleaned_data.get("longitude")

            event = Event(title=title, description=description,
                    start=start, end=end, latitude=latitude, longitude=longitude)
            event.save()

            return redirect("create event")

    form = EventCreationForm()
    return render(request, "game/create_event.html", {"form": form})


def profile(request):
    title = "Profile"
    return render(request, "game/profile.html", {"title": title})
