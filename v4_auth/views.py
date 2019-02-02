from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from v4_player.models import Player
from v4_team.models import Team
from .forms import SignUpForm
from django.utils.timezone import now
from .models import TeamFollowings, PlayerFollowings


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
    return redirect('home')


def follow_player(request, player_id):
    next = request.GET.get('next', '/')
    player = get_object_or_404(Player, id=player_id)
    record = PlayerFollowings.objects.create(user=request.user, player=player)
    record.save()
    return HttpResponseRedirect(next)


def follow_team(request, team_id):
    next = request.GET.get('next', '/')
    team = get_object_or_404(Team, id=team_id)
    record = TeamFollowings.objects.create(user=request.user, team=team)
    record.save()
    return HttpResponseRedirect(next)