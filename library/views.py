from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def hello_name(request):
    name = 'Konstantin'
    return HttpResponse(f"<h1 style='color: #f4ce14; background-color: #495e57; text-align: center;'>Hello, {name}</h1>")

