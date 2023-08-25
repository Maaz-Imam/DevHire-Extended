import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ResumeForm
from django.contrib.auth.decorators import login_required
# from .Interview import *
# import sys
# sys.path.append("..")
# from src import main 
from . import main
from . import Interview
import jsonify
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
def initiate_resume_parsing(request):
    return JsonResponse({"result": True})
    if not request.user.resume:
        return JsonResponse({"result": False})
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_relative_path = "resumes\\AshadAbdullah_resume_DsxBN9s.pdf"
    pdf_full_path = os.path.join(script_dir, pdf_relative_path)
    if os.path.exists(pdf_full_path):
        print(f"The file at {pdf_full_path} exists.")
    else:
        print(f"The file at {pdf_full_path} does not exist.")
    fileName = main.make_json_from_resume(pdf_full_path, request.user.id)
    request.session['resume_json_filename'] = fileName  # Store the filename in the session
    return JsonResponse({"result": True})

@login_required
def interview_bot(request):
    if not request.user.resume:
        return redirect("DevHireBot:get_resume")
    
    return render(request, "DevHireBot/interview_bot.html")

@login_required
def interview_bot_starter(request):
    if request.method == "POST" or request.method == "GET":
        print("Here 1a")
        if not request.user.resume:
            print("Here 2")
            return JsonResponse({"result": False})
        

        json_data = request.body
        # Print or log the JSON data
        print("JSON Body:", json_data)
        
        # You can also decode and print the JSON data as a string
        json_string = json_data.decode('utf-8')
        print("JSON String:", json_string)

        data = json.loads(request.body)  # Parse the JSON data sent in the request body
        prompt = data.get("prompt")

        if data.get("fname"):
            print("Here 3a")
            resume_json_filename = request.session.get('resume_json_filename') # Retrieve the stored filename from the session
        
            if resume_json_filename:
                print("Here 4a")
                return jsonify({"result":Interview.interview_go(resume_json_filename)})
            else:
                print("Here 4b")
                return JsonResponse({"result": False, "error": "Filename not found in session"})
        
        else:
            print("Here 3b")
            return jsonify({"ans":Interview.interview_process(prompt)})

    else:
        print("Here 1b")
        return JsonResponse({'error': 'Invalid request method'}, status=405)