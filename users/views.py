from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

import json
    
# Create your views here.
def username(request):
    """Returns "true" is username exists and "false" if not."""
    username = request.GET.get('username')
    if not username is None and len(username) > 0:
        return HttpResponse(
            str(
                username_exists(username, original=request.user.username)
            ).lower()
        )
    else:
        return HttpResponse("")
    
def profile_redirect(request):
    return redirect("main:index")

def username_exists(username, original=""):
    """Returns true if the given username exists."""
    return username != original and User.objects.filter(username=username).count() > 0