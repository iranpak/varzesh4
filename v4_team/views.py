from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from jdatetime import datetime as jDatetime
import datetime
from operator import attrgetter

from .models import Team
from v4_match.models import Match
from v4_news.models import News
from v4_player.models import Player, Staff


# Create your views here.


def show_team(request, team_name):
    # return HttpResponse(ordering)
    ordering = request.GET.get('ordering', '')
    team = get_object_or_404(Team, name=team_name)
    win_match_list = []
    draw_match_list = []
    lost_match_list = []
    title_news = []
    tags_news = []
    body_news = []
    opp_list = []
    last_games = []
    matches = Match.objects.filter(Q(home_score__isnull=False)&Q(away_score__isnull=False)).all()
    news = News.objects.all()
    send_news = []
    opp_list = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__lte=jDatetime.now())))
                      .all().order_by('-date'))
    for new in news:
        if new.title.__contains__(team.name) or new.title.__contains__(team.persian_name):
            title_news.append(new)
        elif new.body.__contains__(team.name) or new.body.__contains__(team.persian_name):
            body_news.append(new)
        elif new.tags.__contains__(team.name) or new.tags.__contains__(team.persian_name):
            tags_news.append(new)
    for match in matches:
        if match.date < jDatetime.now():
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

    if ordering == '':
        last_games = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__lte=jDatetime.now())))
                      .all().order_by('-date'))
        title_news.extend(tags_news)
        title_news.extend(body_news)
        title_news.sort(key=attrgetter('created_at'), reverse=True)
        send_news = title_news
    elif ordering == 'win':
        last_games = win_match_list
        title_news.extend(tags_news)
        title_news.extend(body_news)
        title_news.sort(key=attrgetter('created_at'), reverse=True)
        send_news = title_news
    elif ordering == 'draw':
        last_games = draw_match_list
        title_news.extend(tags_news)
        title_news.extend(body_news)
        title_news.sort(key=attrgetter('created_at'), reverse=True)
        send_news = title_news
    elif ordering == 'lost':
        last_games = lost_match_list
        title_news.extend(tags_news)
        title_news.extend(body_news)
        title_news.sort(key=attrgetter('created_at'), reverse=True)
        send_news = title_news
    elif ordering == 'title':
        send_news = title_news
        last_games = opp_list
    elif ordering == 'tags':
        send_news = tags_news
        last_games = opp_list
    elif ordering == 'body':
        send_news = body_news
        last_games = opp_list
    else:
        opp_list = []
        for match in matches:
            if match.date < jDatetime.now():
                if match.home == team:
                    if str(match.away) == ordering:
                        opp_list.append(match)
                elif match.away == team:
                    if str(match.home) == ordering:
                        opp_list.append(match)
        last_games = opp_list
    future_five_games = (Match.objects.filter((Q(home=team) | Q(away=team)) & (Q(date__gte=jDatetime.now())))
                         .all().order_by('date'))

    for news in send_news:
        news.body = news.body[:100]
    news = News.objects.filter(tags__contains=team.name).all()
    players = Player.objects.filter(team=team).all()
    staffs = Staff.objects.filter(team=team).all()
    return render(request, 'v4_team/team_page.html',
                  {'team': team, 'news': send_news, 'last_five_games': last_games[:5],
                   'future_five_games': future_five_games[:5], 'team_news': send_news,
                   'players': players, 'staffs': staffs})
