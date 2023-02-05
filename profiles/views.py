from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(args):
    return HttpResponse ("<h1> Test View </H1>")