from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Takes a request and returns a response (called request handler)

def say_hello(request):
    return HttpResponse("Hello")