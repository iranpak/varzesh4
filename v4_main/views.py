from django.db.models import Q
from django.shortcuts import render
from v4_news.models import News
from v4_auth.models import *
import jdatetime


# Create your views here.


def show_main_page(request):
    last_news = News.objects.order_by('-created_at')[:10]
    if request.user.is_authenticated:
        following_news = []
        following_teams = TeamFollowings.objects.filter(user=request.user)
        following_players = PlayerFollowings.objects.filter(user=request.user)
        for team in following_teams:
            team_news = News.objects.filter(
                Q(tags__contains=team.team.name) | Q(tags__contains=team.team.persian_name)).order_by('-created_at')
            for news in team_news:
                if (jdatetime.datetime.now().date() - news.created_at.date()).days <= 2:
                    following_news.append(news)

        for player in following_players:
            player_news = News.objects.filter(
                Q(tags__contains=player.player.lastname) | Q(tags__contains=player.player.get_full_name())).order_by(
                '-created_at')
            for news in player_news:
                if (jdatetime.datetime.now().date() - news.created_at.date()).days <= 2:
                    following_news.append(news)

        return render(request, 'v4_main/homepage.html', {'last_news': last_news, 'following_news': following_news})

    return render(request, 'v4_main/homepage.html', {'last_news': last_news})
