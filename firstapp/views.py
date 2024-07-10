from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.shortcuts import redirect, render

from .forms import EditUserForm, RegisterForm


# Create your views here.
def home(request):
    return render(request, "home.html")


def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html", {"user": request.user})
    else:
        return redirect("login")


def signup(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            messages.success(request, "Account created successfully")
            messages.info(request, "Welcome")
            messages.warning(request, "This is a warning message")
            form.save(commit=True)
            print(form.cleaned_data)

            return redirect("profile")

    else:
        form = RegisterForm()

    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                username=name, password=password
            )  # Check if user exists in the database...
            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                return redirect("signup")
        # else:
        #     return redirect("signup")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

    # user = authenticate(
    #     username=form.cleaned_data["username"],
    #     password=form.cleaned_data["password"],
    # )
    # if user is not None:
    #     login(request, user)
    #     messages.success(request, "You are now logged in")
    #     return redirect("home")
    # else:
    #     messages.error(request, "Invalid credentials")


def user_logout(request):
    logout(request)
    return redirect("login")


def change_password(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("profile")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "change_password.html", {"form": form})


def forget_password(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("profile")
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, "change_password.html", {"form": form})


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                print("Edit Profile", form.cleaned_data)
                return redirect("profile")
        else:
            form = EditUserForm(instance=request.user)
        return render(request, "edit_profile.html", {"form": form})
