import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ResumeForm
from django.contrib.auth.decorators import login_required

from . import main
from . import Interview
import json

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

@login_required
def interview_bot(request):
    if not request.user.resume:
        return redirect("DevHireBot:get_resume")
    
    return render(request, "DevHireBot/interview_bot.html")

@login_required
def interview_bot_starter(request):
    if request.method == "POST" or request.method == "GET":
        if not request.user.resume:
            return JsonResponse({"result": False})

        json_stuff = request.body
        json_string = json_stuff.decode('utf-8')
        print("JSON String:", json_string)

        data = json.loads(request.body)  # Parse the JSON data sent in the request body
        prompt = data.get("prompt")

        if data.get("fname"):
            resume_json_filePath = request.session.get('resume_json_filePath') # Retrieve the stored filename from the session
        
            if resume_json_filePath:
                with open(resume_json_filePath, 'r') as json_file:
                    json_data = json.load(json_file)
                botResponse = Interview.interview_go(request,json_data)
                print(type(botResponse),botResponse)
                return JsonResponse({"result":botResponse})
            else:
                return JsonResponse({"result": False, "error": "Filename not found in session"})
        
        else:
            botResponse = Interview.interview_process(request,prompt)
            return JsonResponse({"ans":botResponse})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)