from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
from .customDecorators import anonymous_required

app_name = "DevHireBot"

urlpatterns = [
    path("", views.index, name="index"),
    
    # Interview related views
    path("get_resume/", views.get_resume, name='get_resume'),
    path("interview_pilot/", views.interview_pilot, name='interview_pilot'),
    path("interview_bot/", views.interview_bot, name='interview_bot'),
    
    # Authentications
    path(
        "accounts/login/",
        anonymous_required(
            auth_views.LoginView.as_view(template_name="accounts/login.html")
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        login_required(
            auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        ),
        name="logout",
    ),
    path(
        "accounts/register/",
        anonymous_required(views.register),
        name="register",
    ),

    # API
    path("initiate_resume_parsing", views.initiate_resume_parsing, name="initiate_resume_parsing"),
    path("interview_bot_starter/", views.interview_bot_starter, name="interview_bot_starter")
]
