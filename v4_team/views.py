from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from jdatetime import datetime as jDatetime
import datetime

from .models import Team
from v4_match.models import Match
from v4_news.models import News


# Create your views here.


def show_team(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    last_five_games = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__lte=jDatetime.now())))
                       .all().order_by('-date'))[:5]
    future_five_games = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__gte=jDatetime.now())))
                         .all().order_by('date'))[:5]
    team_news = (News.objects.filter((Q(tags__contains=str(team)) | Q(tags__contains=team_name)))).all().order_by(
        '-created_at')
    for news in team_news:
        news.body = news.body[:100]
    news = News.objects.filter(tags__contains=team.name).all()
    return render(request, 'v4_team/team_page.html', {'team': team, 'news': news, 'last_five_games': last_five_games,
                                                      'future_five_games': future_five_games, 'team_news': team_news})
