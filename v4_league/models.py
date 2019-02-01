from django.db import models
from django.core.validators import *
from v4_team.models import Team
from django.dispatch import receiver


class League(models.Model):
    name = models.CharField(max_length=64)
    teams = models.ManyToManyField(Team, related_name='teams')
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.name + ' ' + self.year

    class Meta:
        unique_together = ('name', 'year')


# class TeamsOfLeague(models.Model):
#     league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league')
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
#     team_score = models.IntegerField(default=0)
#     team_difference = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.league.name + '-' + self.team.persian_name
#
#
# def create_teams_of_league_models(instance, **kwargs):
#     for team in instance.teams.all():
#         record = TeamsOfLeague.objects.create(league=instance, team=team)
#         record.save()
#
#
# models.signals.m2m_changed.connect(create_teams_of_league_models, sender=League.teams.through)
