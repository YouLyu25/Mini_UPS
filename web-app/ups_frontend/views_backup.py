from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Person
from .models import Event
from .models import Question
from .models import Guest
from .models import Vender
from .models import Response
import json
from django.core import serializers


def login(request):
    return render(request,"login.html")

def regist(request):
    return render(request, "regist.html")

def user(request):
    return render(request, "user.html")

def Userinterface(request):
    return render(request, "Userinterface.html")


def authentication(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponse("Invalid user name or wrong password, please try again!")
    else:
        auth.login(request, user)
        return HttpResponse("login succeed! welcome!")

def logout(request):
    info = request.POST.get("info")
    if info == "logout":
        auth.logout(request)
        return HttpResponse("user successfully logs out!")
    return HttpResponse("failed")

def addUser(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    secondPassword = request.POST.get('secondPassword')
    user = User.objects.filter(username__exact=username)
    if not user:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        #person = Person.objects.create(username=username, email=email)
        #person.save()
        return HttpResponse("successfully registered!")
    else:
        return HttpResponse("username already exists, please choose a cooler name!")
