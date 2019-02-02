from django.db import models
from django.contrib.auth.models import User
from v4_player.models import Player
from v4_team.models import Team


class TeamFollowings(models.Model):
    user = models.ForeignKey(User, related_name='team_user', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('user', 'team')


class PlayerFollowings(models.Model):
    user = models.ForeignKey(User, related_name='player_user', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='player', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('user', 'player')

