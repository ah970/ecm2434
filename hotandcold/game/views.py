from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Home page.")


def login(request):
    return render(request, "game/loginScreen.html", None)


def register(request):
    return render(request, "game/accountCreation.html", None) 


def game(request):
    return HttpResponse("Game page.")


def profile(request):
    return HttpResponse("User profile page.")
