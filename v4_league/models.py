from django.db import models
from django.core.validators import *


class League(models.Model):
    name = models.CharField(max_length=64)
    number_of_teams = models.IntegerField()
    year = models.IntegerField(validators=[MinValueValidator(1320), MaxValueValidator(1500)])

    def get_league_fullname(self):
        return self.name + ' - ' + str(self.year)
