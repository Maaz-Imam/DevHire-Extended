import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ResumeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "DevHireBot/index.html")


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
            user = request.user

            if user.resume:
                # Delete the old resume file if it exists
                user.resume.delete()

            user.resume = uploaded_file
            user.save()

            return redirect('DevHireBot:interview_pilot')
        else:
            messages.error(request, form.errors)
    
    else:  # GET request
        form_data = {'resume': request.user.resume} if request.user.resume else None
        form = ResumeForm(initial=form_data)

    return render(request, "DevHireBot/data.html", {'form': form, 'resume_name': os.path.basename(request.user.resume.name) if request.user.resume else None})

@login_required
def interview_pilot(request):
    if not request.user.resume:
        return redirect("DevHireBot:get_resume")
        
    return render(request, "DevHireBot/interview_pilot.html")