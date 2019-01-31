from django.shortcuts import render, get_object_or_404
from .models import Player
from v4_news.models import News
from django.db.models import Q

# Create your views here.


def show_homepage(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    related_news = News.objects.filter(Q(tags__contains=player.firstname) | Q(tags__contains=player.lastname)).all()
    for r in related_news:
        print(r.title)
    return render(request, 'v4_player/homepage.html', {'player': player, 'news': related_news})