from django.db import models
from django.core.validators import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

from v4_team.models import Team
from django.dispatch import receiver


class League(models.Model):
    name = models.CharField(max_length=64)
    teams = models.ManyToManyField(Team, related_name='teams')
    year = models.IntegerField(validators=[MinValueValidator(1320), MaxValueValidator(2200)])

    def get_league_fullname(self):
        return self.name + ' - ' + str(self.year)

    def __str__(self):
        return self.name


class TeamsOfLeague(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    team_score = models.IntegerField(default=0)
    team_difference = models.IntegerField(default=0)

    def __str__(self):
        return self.league.name + '-' + self.team.persian_name


def create_teams_of_league_models(instance, **kwargs):
    for team in instance.teams.all():
        record = TeamsOfLeague.objects.create(league=instance, team=team)
        record.save()


def update_teams_of_league_score(instance, **kwargs):
    match = instance.match
    league = match.league
    if instance.type == 'گل':
        scorer_team = get_object_or_404(Team, id=instance.player1.team.id)
        if match.home == scorer_team:
            conceding_team = match.away
        else:
            conceding_team = match.home
        team_of_league = get_object_or_404(TeamsOfLeague, (Q(league=league) & Q(team=scorer_team)))
        team_of_league_conceding = get_object_or_404(TeamsOfLeague, (Q(league=league) & Q(team=scorer_team)))
        team_of_league.team_score = team_of_league.team_score + 1
        team_of_league_conceding = team_of_league_conceding.te
        if match.home == team:
            match.home_score = match.home_score + 1
        elif match.away == team:
            match.away_score = match.away_score + 1
    match.save()
    stats = match.footballstats_set.all()[0]
    if stats.match.home == team:
        stats.score_home = stats.score_home + 1
    elif stats.match.away == team:
        stats.away_score = stats.away_score + 1
    stats.save()

models.signals.m2m_changed.connect(create_teams_of_league_models, sender=League.teams.through)
