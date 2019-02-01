from django.db import models
from django_jalali.db import models as jModels
from django.shortcuts import get_object_or_404
from django.db.models import Q
import jdatetime
# Create your models here.
from v4_team.models import Team
from v4_player.models import Player
from v4_league.models import League


class Match(models.Model):
    home = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name='home_team')
    away = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name='away_team')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    date = jModels.jDateTimeField(default=jdatetime.datetime.now)
    MOTM = models.ForeignKey(to=Player, null=True, on_delete=models.CASCADE, blank=True)
    league = models.ForeignKey(to=League, null=True, blank=True, on_delete=models.CASCADE)
    week = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.home.name + ' - ' + self.away.name + '\t' + str(self.date.date())

    def get_match_info(self):
        toR = ""
        if self.week is not None:
            toR += "هفته " + str(self.week) + " ام " + str(self.league)
        elif self.description:
            toR += self.description + "لیگ " + str(self.league)
        return toR

    def get_yellow_cards_home(self):
        yellow_cards_home_events = Event.objects.filter(
            Q(match=self) & Q(type='کارت زرد') & Q(player1__team=self.home)).all().count()
        return yellow_cards_home_events

    def get_yellow_cards_away(self):
        yellow_cards_home_events = Event.objects.filter(
            Q(match=self) & Q(type='کارت زرد') & Q(player1__team=self.away)).all().count()
        return yellow_cards_home_events

    def get_red_cards_home(self):
        red_cards_home_events = Event.objects.filter(
            Q(match=self) & Q(type='کارت قرمز') & Q(player1__team=self.home)).all().count()
        return red_cards_home_events

    def get_red_cards_away(self):
        red_cards_home_events = Event.objects.filter(
            Q(match=self) & Q(type='کارت قرمز') & Q(player1__team=self.away)).all().count()
        return red_cards_home_events


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
    possession_home = models.FloatField(default=0, null=True, blank=True)
    possession_away = models.FloatField(default=0, null=True, blank=True)
    offsides_home = models.IntegerField(default=0, null=True, blank=True)
    offsides_away = models.IntegerField(default=0, null=True, blank=True)
    saves_home = models.IntegerField(default=0, null=True, blank=True)
    saves_away = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.match


class BasketballStats(Stats):
    player = models.ForeignKey(to=Player, null=True, blank=True, on_delete=models.CASCADE)
    dribbles = models.IntegerField(null=True, blank=True)
    blocks = models.IntegerField(null=True, blank=True)
    steals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)


class EventIcon(models.Model):
    icon = models.ImageField(upload_to='resources/images/event-icons')
    event_types = (('گل', 'goal'), ('پاس گل', 'assist'), ('تعویض', 'substitute'), ('کارت قرمز', 'red-card'),
                   ('کارت زرد', 'yellow-card'), ('پرتاب سه امتیازی', '3-points-shot'),
                   ('پرتاب دو امتیازی', 'areal-shot'), ('توپ ربایی', 'steal'))
    event_type = models.CharField(max_length=100, choices=event_types)

    def __str__(self):
        return self.event_type


class Event(models.Model):
    event_types = (('گل', 'goal'), ('پاس گل', 'assist'), ('تعویض', 'substitute'), ('کارت قرمز', 'red-card'),
                   ('کارت زرد', 'yellow-card'), ('پرتاب سه امتیازی', '3-points-shot'),
                   ('پرتاب دو امتیازی', 'areal-shot'), ('توپ ربایی', 'steal'))
    type = models.CharField(max_length=100, choices=event_types)
    event_icon = models.ForeignKey(to=EventIcon, on_delete=models.CASCADE)
    match = models.ForeignKey(to=Match, null=False, on_delete=models.CASCADE)
    player1 = models.ForeignKey(to=Player, null=False, on_delete=models.CASCADE, related_name='change_out')
    player2 = models.ForeignKey(to=Player, null=True, blank=True, on_delete=models.CASCADE, related_name='change_in')
    is_successful = models.BooleanField(default=True, null=False)
    minute = models.IntegerField(blank=False, null=False)
    part_of_game = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.match) + str(self.minute)

    def get_home_or_away(self):
        try:
            self.match.home.player_set.get(id=self.player1.id)
            return ''
        except Exception:
            return ' team-2'

    def is_two_players(self):
        if self.type == 'تعویض':
            return True
        return False


def update_match_score(instance, **kwargs):
    match = instance.match
    team = get_object_or_404(Team, id=instance.player1.team.id)
    if instance.type == 'گل':
        if match.home == team:
            match.home_score = match.home_score + 1
        elif match.away == team:
            match.away_score = match.away_score + 1
    match.save()
    stats = match.footballstats_set.all()[0]
    if stats.match.home == team:
        stats.score_home = stats.score_home + 1
    elif stats.match.away == team:
        stats.away_score = stats.score_away + 1
    stats.save()


models.signals.post_save.connect(update_match_score, sender=Event)


class Lineup(models.Model):
    player = models.ForeignKey(to=Player, null=False, on_delete=models.CASCADE)
    match = models.ForeignKey(to=Match, null=False, on_delete=models.CASCADE)
    is_starter = models.BooleanField(default=True, null=False, blank=False)


class Multimedia(models.Model):
    multimedia_types = (('pic', 'image'), ('clip', 'video'))
    match = models.ForeignKey(to=Match, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=multimedia_types)
    file = models.FileField(upload_to='resources/images/multimedias')
    caption = models.CharField(max_length=4000, null=True, blank=True)
    upload_time = jModels.jDateTimeField(default=jdatetime.datetime.now)
    link = models.CharField(max_length=4000, blank=True, null=True)

    def __str__(self):
        return str(self.match) + self.caption[:50]


class Commentary(models.Model):
    match = models.ForeignKey(to=Match, on_delete=models.CASCADE)
    text = models.CharField(max_length=4000)
    minute = models.IntegerField()

    def __str__(self):
        return str(self.match) + ' (' + self.text[:30] + '...)'
