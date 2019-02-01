from re import match

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from v4_match.models import *
from jdatetime import datetime as jDatetime

# Create your views here.
from v4_news.models import News


def show_match_page(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    events = Event.objects.filter(match=match).order_by('minute').all()
    match_stats = get_object_or_404(FootballStats, match=match)
    home_lineup_starters = Lineup.objects.filter(
        (Q(player__team=match.home) & Q(match=match) & Q(is_starter=True))).all().order_by('player__current_number')
    away_lineup_starters = Lineup.objects.filter(
        (Q(player__team=match.away) & Q(match=match) & Q(is_starter=True))).all().order_by('player__current_number')
    home_lineup_subs = Lineup.objects.filter(
        (Q(player__team=match.away) & Q(match=match) & Q(is_starter=False))).all().order_by('player__current_number')
    away_lineup_subs = Lineup.objects.filter(
        (Q(player__team=match.away) & Q(match=match) & Q(is_starter=False))).all().order_by('player__current_number')
    commentaries = Commentary.objects.filter(match=match).all().order_by('-minute')
    match_news = News.objects.filter(Q(tags__contains=match.home.persian_name) & Q(tags__contains=match.away.persian_name)).all().order_by('-created_at')
    multimedias = Multimedia.objects.filter(match=match).all().order_by('type')
    return render(request, 'v4_match/match_page.html',
                  {'match': match, 'events': events, 'match_stats': match_stats, 'home_lineup': home_lineup_starters,
                   'away_lineup': away_lineup_starters, 'home_subs': home_lineup_subs, 'away_subs': away_lineup_subs,
                   'commentaries': commentaries, 'match_news': match_news, 'multimedias': multimedias})
