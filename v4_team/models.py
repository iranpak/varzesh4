from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(null=True, blank=True)
    special_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name



