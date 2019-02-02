from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from jdatetime import datetime as jDatetime
import datetime

from .models import Team
from v4_match.models import Match
from v4_news.models import News
from v4_player.models import Player, Staff


# Create your views here.


def show_team(request, team_name, ordering=None):
    # return HttpResponse(ordering)
    team = get_object_or_404(Team, name=team_name)
    win_match_list = []
    draw_match_list = []
    lost_match_list = []
    opp_list = []
    last_games = []
    matches = Match.objects.filter(Q(home_score__isnull=False)&Q(away_score__isnull=False)).all()
    for match in matches:
        if match.home == team:
            if match.home_score > match.away_score:
                win_match_list.append(match)
            elif match.home_score == match.away_score:
                draw_match_list.append(match)
            else:
                lost_match_list.append(match)
        elif match.away == team:
            if match.home_score < match.away_score:
                win_match_list.append(match)
            elif match.home_score == match.away_score:
                draw_match_list.append(match)
            else:
                lost_match_list.append(match)

    if ordering is None:
        last_games = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__lte=jDatetime.now())))
                           .all().order_by('-date'))
    elif ordering == 'win':
        last_games = win_match_list
    elif ordering == 'draw':
        last_games = draw_match_list
    elif ordering == 'lost':
        last_games = lost_match_list
    else:
        for match in matches:
            if match.home == team:
                if str(match.away) == ordering:
                    opp_list.append(match)
            elif match.away == team:
                if str(match.home) == ordering:
                    opp_list.append(match)
        last_games = opp_list
    future_five_games = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__gte=jDatetime.now())))
                         .all().order_by('date'))
    team_news = (News.objects.filter((Q(tags__contains=str(team)) | Q(tags__contains=team_name)))).all().order_by(
        '-created_at')
    for news in team_news:
        news.body = news.body[:100]
    news = News.objects.filter(tags__contains=team.name).all()
    players = Player.objects.filter(team=team).all()
    staffs = Staff.objects.filter(team=team).all()
    return render(request, 'v4_team/team_page.html', {'team': team, 'news': news, 'last_five_games': last_games[:5],
                                                      'future_five_games': future_five_games, 'team_news': team_news,
                                                      'players': players, 'staffs': staffs})
