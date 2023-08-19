from django.shortcuts import redirect
from django.urls import reverse

def anonymous_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('DevHireBot:index'))  # Redirect to your desired page
        return view_func(request, *args, **kwargs)
    return _wrapped_view
