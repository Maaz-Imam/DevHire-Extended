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
]
