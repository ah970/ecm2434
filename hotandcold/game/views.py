from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Home page.")


def login(request):
    return HttpResponse("Login page.")


def register(request):
    return HttpResponse("Registration page.")


def game(request):
    return HttpResponse("Game page.")
