from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")  # change to your login url name
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
