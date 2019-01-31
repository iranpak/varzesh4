from django.db import models
from django_jalali.db import models as jModels
import jdatetime
# Create your models here.
from v4_team.models import Team
from v4_player.models import Player
from v4_league.models import League


class Match(models.Model):
    home = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name='host_team')
    away = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name='away_team')
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    date = jModels.jDateTimeField(default=jdatetime.datetime.now)
    MOTM = models.ForeignKey(to=Player, null=True, on_delete=models.CASCADE, blank=True)
    league = models.ForeignKey(to=League, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.home.name + ' - ' + self.away.name + '\t' + str(self.date.date())


class Stats(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    fouls_home = models.IntegerField(default=0, null=True)
    fouls_away = models.IntegerField(default=0, null=True)
    score_home = models.IntegerField(default=0, null=True)
    score_away = models.IntegerField(default=0, null=True)

    class Meta:
        abstract = True


class FootballStats(Stats):
    shots_away = models.IntegerField(default=0, null=True, blank=True)
    shots_home = models.IntegerField(default=0, null=True, blank=True)
    corner_home = models.IntegerField(default=0, null=True, blank=True)
    corner_away = models.IntegerField(default=0, null=True, blank=True)
    shots_on_target_home = models.IntegerField(default=0, null=True, blank=True)
    shots_on_target_away = models.IntegerField(default=0, null=True, blank=True)
    possession_home = models.IntegerField(default=0, null=True, blank=True)
    possession_away = models.IntegerField(default=0, null=True, blank=True)


class BasketballStats(Stats):
    player = models.ForeignKey(to=Player, null=True, blank=True, on_delete=models.CASCADE)
    dribbles = models.IntegerField(null=True, blank=True)
    blocks = models.IntegerField(null=True, blank=True)
    steals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)


class Event(models.Model):
    type = models.CharField(max_length=100)
    match = models.ForeignKey(to=Match, null=False, on_delete=models.CASCADE)
    player1 = models.ForeignKey(to=Player, null=False, on_delete=models.CASCADE, related_name='change_out')
    player2 = models.ForeignKey(to=Player, null=True, blank=True, on_delete=models.CASCADE, related_name='change_in')
    is_successful = models.BooleanField(default=True, null=False)
    minute = models.TimeField(null=False)
    part_of_game = models.IntegerField(null=True, blank=True)


class Lineup(models.Model):
    player = models.ForeignKey(to=Player, null=False, on_delete=models.CASCADE)
    match = models.ForeignKey(to=Match, null=False, on_delete=models.CASCADE)
    is_starter = models.BooleanField(default=True, null=False, blank=False)


class Multimedia(models.Model):
    multimedia_types = (('pic', 'image'), ('clip', 'video'))
    match = models.ForeignKey(to=Match, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=multimedia_types)
    file = models.FileField()
    caption = models.CharField(max_length=4000, null=True, blank=True)
    upload_time = jModels.jDateTimeField(default=jdatetime.datetime.now)


class Commentary(models.Model):
    match = models.ForeignKey(to=Match, on_delete=models.CASCADE)
    text = models.CharField(max_length=4000)
    minute = models.TimeField()
