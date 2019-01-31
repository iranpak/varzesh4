from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100)
    persian_name = models.CharField(max_length=100, null=True, blank=True, default='')
    logo = models.ImageField(null=True, blank=True, upload_to='resources/images/teams/team_logo')
    special_pic = models.ImageField(null=True, blank=True, upload_to='resources/images/teams/special_images')

    def __str__(self):
        return self.persian_name
