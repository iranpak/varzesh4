# Generated by Django 2.1.4 on 2019-02-01 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v4_league', '0004_auto_20190131_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1320), django.core.validators.MaxValueValidator(2200)]),
        ),
    ]
