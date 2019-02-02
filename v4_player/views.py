from django.shortcuts import render, get_object_or_404

from v4_match.models import Event, Match, Lineup, FootballStats
from .models import Player
from v4_news.models import News
from django.db.models import Q

# Create your views here.


class PlayerStats:
    def __init__(self):
        self.clean_sheets = 0
        self.goals = 0
        self.assists = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.saves = 0
        self.conceding_goal = 0


def show_homepage(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    related_news = News.objects.filter(Q(tags__contains=player.firstname) | Q(tags__contains=player.lastname)).all()
    stats = PlayerStats()
    events = Event.objects.filter(player1=player)
    for event in events:
        if event.type == 'گل':
            stats.goals += 1
        elif event.type == 'پاس گل':
            stats.assists += 1
        elif event.type == 'کارت زرد':
            stats.yellow_cards += 1
        elif event.type == 'کارت قرمز':
            stats.red_cards += 1
    lineups = Lineup.objects.filter(player=player).all()
    fix_games = []
    for lineup in lineups:
        fix_games.append(lineup.match)
        stat = get_object_or_404(FootballStats, match=lineup.match)
        if player.team == lineup.match.home:
            stats.saves += stat.saves_home
            if lineup.match.away_score == 0:
                stats.clean_sheets += 1
            elif lineup.match.away_score > 0:
                stats.conceding_goal += lineup.match.away_score
        elif player.team == lineup.match.away:
            stats.saves += stat.saves_away
            if lineup.match.home_score == 0:
                stats.clean_sheets += 1
            elif lineup.match.home_score > 0:
                stats.conceding_goal += lineup.match.home_score

    for r in related_news:
        print(r.title)
    return render(request, 'v4_player/homepage.html', {'player': player, 'news': related_news, 'stats': stats})
