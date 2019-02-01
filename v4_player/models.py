from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
from v4_team.models import Team


class Person(models.Model):
    firstname = models.CharField(max_length=100, default='')
    lastname = models.CharField(max_length=100, default='')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    age = models.IntegerField()
    sport = models.SmallIntegerField()
    nationality = models.CharField(max_length=30, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to='resources/images/players')

    class Meta:
        abstract = True

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def get_full_name(self):
        return self.firstname + ' ' + self.lastname


class Player(Person):
    is_right_foot = models.BooleanField(default=True)
    post = models.CharField(max_length=30)
    height = models.IntegerField()
    weight = models.IntegerField()
    current_number = models.IntegerField(null=True, blank=True)
    overall_power = models.IntegerField(validators=[MinValueValidator(40), MaxValueValidator(99)], null=True, blank=True)


class Staff(Person):
    post = models.CharField(max_length=100)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

