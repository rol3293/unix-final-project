import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse


@login_required
def index(request):
    users = User.objects.all()
    return render(request, "project/index.html", {
        "current_user": request.user,
        "users": users
    })


def login_view(request):
    if request.method == "POST":
        # parse request json info
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body["username"]
        password = body["password"]

        # try to authenticate
        user = authenticate(username=username, password=password)
        if user is not None:  # success
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:  # fail
            return JsonResponse({
                "error": "Wrong credentials"
            }, status=401)
    else:
        return render(request, "project/login.html")


def signup(request):
    if request.method == "POST":
        # parse request json info
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body["username"]
        password = body["password"]
        vpassword = body["vpassword"]

        # check if password and vpassword are the same
        if password != vpassword:
            return JsonResponse({
                "error": "Password and password verification are not equal"
            })

        # check if username is not taken
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, None, password)
            user.save()
            return HttpResponseRedirect(reverse("index"))
        else:  # if username is already taken, return a error message
            return JsonResponse({
                "error": "Username is already taken"
            })
    else:
        return render(request, "project/signup.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
