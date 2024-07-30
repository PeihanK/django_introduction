from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def hello_name(request):
    name = 'Konstantin'
    return HttpResponse(f"<h1 style='color: #f4ce14; background-color: #495e57; text-align: center;'>Hello, {name}</h1>")


def first_view(request):
    return HttpResponse("<h1>Hello, world. You're at the polls view.</h1>")


def second_view(request):
    return HttpResponse("<h1>Hello, world. It's second view.</h1>")
