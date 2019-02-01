from django.shortcuts import render, get_object_or_404
from .models import League
from v4_match.models import Match
from django.db.models import Q
from operator import attrgetter

# from v4


# Create your views here.

class TeamModel():
    def __init__(self, model, number_of_matches, win, lose, tie, scored_goals, received_goals, score):
        self.model = model
        self.number_of_matches = number_of_matches
        self.win = win
        self.lose = lose
        self.tie = tie
        self.scored_goals = scored_goals
        self.received_goals = received_goals
        self.goal_difference = scored_goals - received_goals
        self.score = score


def show_league_page(request, league_id):
    league = get_object_or_404(League, id=league_id)
    teams_models = league.teams.all()
    teams = []

    for team in teams_models:
        team_matches = get_team_matches(team, league)
        winner_data = calculate_number_of_win_and_lose(team, team_matches)
        team_score = winner_data['win']*3 + winner_data['tie']
        team_goals = calculate_number_of_goals(team, team_matches)
        team_model = TeamModel(team, len(team_matches), winner_data['win'], winner_data['lose'], winner_data['tie'],
                               team_goals['scored_goals'], team_goals['received_goals'], team_score)
        teams.append(team_model)

    teams.sort(key=attrgetter('score', 'goal_difference'), reverse=True)
    return render(request, 'v4_league/league_page.html', {'league': league, 'teams': teams})


def get_team_matches(team, league):
    team_matches = Match.objects.filter((Q(home=team) | Q(away=team)) & Q(league=league)).all()
    return team_matches


def calculate_number_of_win_and_lose(team, team_matches):
    games_won = 0
    lost_games = 0
    tie_games = 0
    for match in team_matches:
        if match.home_score == match.away_score:
            tie_games += 1

        if team.persian_name == match.home.persian_name:
            if match.home_score > match.away_score:
                games_won += 1
            elif match.away_score > match.home_score:
                lost_games += 1

        elif team.persian_name == match.away.persian_name:
            if match.home_score > match.away_score:
                lost_games += 1
            elif match.away_score > match.home_score:
                games_won += 1

    return {'win': games_won, 'lose': lost_games, 'tie': tie_games}


def calculate_number_of_goals(team, team_matches):
    scored_goals = 0
    received_golas = 0
    for match in team_matches:
        if team.persian_name == match.home.persian_name:
            scored_goals += match.home_score
            received_golas += match.away_score
        elif team.persian_name == match.away.persian_name:
            received_golas += match.home_score
            scored_goals += match.away_score

    return {'scored_goals': scored_goals, 'received_goals': received_golas}
