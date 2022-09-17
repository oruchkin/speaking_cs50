from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseRedirect
from django.urls import reverse    
from django.db import IntegrityError
from .models import User


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "spapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "spapp/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if len(username) < 4:
            return render(request, "spapp/register.html", {
                "message": "The username must be at least 4 letters long"
            })
        if len(username) > 14:
            return render(request, "spapp/register.html", {
                "message": "The username must be no more than 15 letters long"
            })
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "spapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "spapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "spapp/register.html")