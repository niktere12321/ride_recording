from django.shortcuts import redirect
from django.urls import reverse


def active(func):
    def check_active(request, *args, **kwargs):
        if request.user.active == True:
            return func(request, *args, **kwargs)
        return redirect(reverse('users:help_active'))
    return check_active
