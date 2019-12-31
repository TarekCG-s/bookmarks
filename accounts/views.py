from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegistrationForm


def LoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated Successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Inavlid username or password")
    else:
        form = UserLoginForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return render(request, "accounts/register_done.html")
    form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


@login_required
def dashboard(request):
    context = {
        "section": "dashboard",
    }
    return render(request, "accounts/dashboard.html", context)
