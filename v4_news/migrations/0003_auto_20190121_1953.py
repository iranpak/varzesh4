# Generated by Django 2.1.4 on 2019-01-21 19:53

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('v4_news', '0002_auto_20190121_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime.now),
        ),
    ]
