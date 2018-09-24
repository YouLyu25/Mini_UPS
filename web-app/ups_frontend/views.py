from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django import forms
from .models import Person
from .models import package
from .models import item
from .models import time
from .models import Accounts
from .models import curr_world
import json
from django.core import serializers


def login(request):
    return render(request,"login.html")

def regist(request):
    return render(request, "regist.html")

def search(request):
    return render(request, "track.html")

def user(request):
    return render(request, "user.html")

def list(request):
    result1 = curr_world.objects.filter(name="curr_world")
    Worldid = result1[0].worldid
    result = package.objects.filter(username=request.user.username,worldid=Worldid) 
    ans = []
    for tuple in result:
        temp = []
        temp.append(tuple.trackingid)
        if tuple.status is 'C':
            temp.append('Created')
        elif tuple.status is 'E':
            temp.append('Truck en route to warehouse')
        elif tuple.status is 'W':
            temp.append('Truck waiting for packages')
        elif tuple.status is 'L':
            temp.append('Loaded and waiting for delivery')
        elif tuple.status is 'O':
            temp.append('Out for delivery')
        else:
            temp.append('Delivered')
        if tuple.status is 'O' or tuple.status is 'D':
            temp.append(0)
        else:
            temp.append(1)
        temp.append(tuple.position_x)
        temp.append(tuple.position_y)
        ans.append(temp)     
    return HttpResponse(json.dumps(ans))

def showitem(request):
    Trackingid = request.POST.get("trackingid")
    result1 = curr_world.objects.filter(name="curr_world")
    Worldid = result1[0].worldid
    result = item.objects.filter(trackingid = Trackingid, worldid = Worldid)
    ans = []
    if not any (result):
        a = 3 
    else:
        for tuple in result:
            temp = []
            temp.append(tuple.iteminfo)
            temp.append(tuple.count)
            ans.append(temp)
    return HttpResponse(json.dumps(ans)) 

def showhistory(request):
    result1 = curr_world.objects.filter(name="curr_world")
    Worldid = result1[0].worldid
    Trackingid = request.POST.get("trackingid")
    result = time.objects.filter(trackingid = Trackingid, worldid = Worldid)
    temp = []
    ans = []
    temp.append("Package created:")
    temp.append(result[0].c_time)
    ans.append(temp)
    temp1 = []
    temp1.append("Truck to warehouse:")
    temp1.append(result[0].e_time)
    ans.append(temp1)
    temp2 = []
    temp2.append("Truck waiting for package:")
    temp2.append(result[0].w_time)
    ans.append(temp2)
    temp4 = []
    temp4.append("Truck loaded:")
    temp4.append(result[0].l_time)
    ans.append(temp4)
    temp3 = []
    temp3.append("Truck out for delivery:")
    temp3.append(result[0].o_time)
    ans.append(temp3)
    temp5 = []
    temp5.append("package delivered:")
    temp5.append(result[0].d_time)
    ans.append(temp5)
    return HttpResponse(json.dumps(ans))

def track(request):
    result1 = curr_world.objects.filter(name="curr_world")
    Worldid = result1[0].worldid
    Trackingid = request.POST.get("trackingid")
    result = package.objects.filter(trackingid=Trackingid,worldid=Worldid)
    ans = []
    if not any (result):
        temp = []
        temp.append(Trackingid)
        temp.append(" not found!")
        ans.append(temp)
    else:
        temp = []
        temp.append(result[0].trackingid)
        if result[0].status is 'C':
            temp.append('Created')
        elif result[0].status is 'E':
            temp.append('Truck en route to warehouse')
        elif result[0].status is 'W':
            temp.append('Truck waiting for packages')
        elif result[0].status is 'L':
            temp.append('Loaded and waiting for delivery')
        elif result[0].status is 'O':
            temp.append('Out for delivery')
        else:
            temp.append('Delivered')
        ans.append(temp) 
    return HttpResponse(json.dumps(ans))

def post(request):
    Trackingid = request.POST.get("trackingid")
    pos_x = request.POST.get("pos_x")
    pos_y = request.POST.get("pos_y")
    res = package.objects.filter(trackingid=Trackingid)
    if res[0].status is 'O':
        return HttpResponse("Failure because the truck has already on the delivery!")
    else:
        res.update(position_x = pos_x, position_y = pos_y) 
        return HttpResponse("Tracking id: " + Trackingid + " update Successfully!")

def sendemail(request):
    #Trackingid = request.POST.get("trackingid")
    print("abc")
    send_mail('Dear the greatest lordy','You are the king of North!','zhongyuli@gmail.com',['zl158@duke.edu'],fail_silently=False,)  
    return render(request,"login.html")

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
    amazon_account = request.POST.get('Amazon_account') 
    pos_x = request.POST.get('Pos_x')
    pos_y = request.POST.get('Pos_y')
    user = User.objects.filter(username__exact=username)
    if not user:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        account = Accounts.objects.create(ups_account=username, amazon_account=amazon_account,pos_x=pos_x,pos_y=pos_y)
        account.save()
        return HttpResponse("successfully registered!")
    else:
        return HttpResponse("username already exists, please choose a cooler name!")
