from django.http import HttpResponse
from django.shortcuts import render
import os
import operator

def home(request):
    #pwd = os.getcwd()
    #name = 'Ivan'
    return render(request, "home.html")