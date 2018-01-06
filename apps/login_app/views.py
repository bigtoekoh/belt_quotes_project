from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login_app/index.html')

def login(request):
    response = User.objects.login_validator(request.POST)
    if response["status"] == False:
        for val in response["errors"]:
            messages.error(request, val, extra_tags="Login")
        return redirect('/')
    else:
        request.session["user"] = response["user"].id
        return redirect('/quotes')

def registration(request):
    response = User.objects.registration_validator(request.POST)
    if response["status"] == False:
        for val in response["errors"]:
            messages.error(request, val, extra_tags="Registration")
        return redirect('/')
    else:
        request.session["user"] = response["user"].id
        return redirect('/quotes')
