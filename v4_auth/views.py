from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'v4_auth/signup.html', {'form': form})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'v4_auth/login.html')

    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            # [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
            login(request, user)
        else:
            ip_address = request.META['REMOTE_ADDR']
            browser = request.META['HTTP_USER_AGENT']
            current_time = now()

        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')
