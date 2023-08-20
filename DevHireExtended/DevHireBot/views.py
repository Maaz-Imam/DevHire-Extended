from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ResumeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "DevhireBot/index.html")


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("DevHireBot:index")
        else:
            messages.error(request, form.errors)
            return render(
                request,
                "accounts/register.html",
                {"form": SignUpForm(request.POST)},
            )
    else:
        if request.user.is_authenticated:
            return redirect("DevHireBot:index")
        else:
            return render(
                request, "accounts/register.html", {"form": SignUpForm()}
            )

@login_required
def get_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume']
            request.user.resume = uploaded_file
            request.user.save()
            
            return render(request, "DevhireBot/interview.html")
        else:
            messages.error(request, form.errors)
    return render(request, "DevhireBot/data.html", {'form': ResumeForm()})