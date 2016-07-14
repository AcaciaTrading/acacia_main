from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib import auth, messages
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

# Create your views here.
@login_required
def index(request):
    return render(request, "exchanges_website/dashboard.html", {})

def new_token(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    token = Token.objects.create(user=request.user)
    token.save()
    messages.success(request, "New token generated.")
    return redirect('exchanges_website:index')