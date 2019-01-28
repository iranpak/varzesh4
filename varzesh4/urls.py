"""varzesh4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from v4_main import views as main_views
from v4_player import views as player_views
from v4_news import views as news_views
from v4_league import views as league_views
from v4_team import views as team_views
from v4_match import views as match_views
from v4_auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.show_main_page, name='home'),
    path('signup/', auth_views.signup, name='signup'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('player/', player_views.show_homepage, name='player_homepage'),
    path('news/<int:news_id>', news_views.show_news_page, name='news_page'),
    path('league/', league_views.show_league_page, name='league_page'),
    path('player/', player_views.show_homepage, name='player_homepage'),
    path('team/', team_views.show_team),
    path('match/', match_views.show_match_page),
]
