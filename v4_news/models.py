from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels
from datetime import datetime
import jdatetime
from varzesh4.settings import STATIC_URL

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=64, unique=True)
    body = models.CharField(max_length=2048)
    image = models.ImageField(upload_to='resources/images/news')
    sources = models.CharField(max_length=512)
    tags = models.CharField(max_length=512, null=True)
    created_at = jmodels.jDateTimeField(default=jdatetime.datetime.now)

    def __str__(self):
        return self.title

    def get_date(self):
        toR = ""
        deltatime = self.created_at.timestamp()
        time = jdatetime.datetime.now().timestamp()
        days_differential = deltatime / 86400.0
        if 1 > days_differential > 0:
            toR = str(deltatime / 3600.0) + " ساعت قبل"
        else:
            toR = str(deltatime) + " روز قبل"
        return toR