# Generated by Django 2.1.4 on 2019-01-31 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v4_team', '0003_team_persian_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='persian_name',
            field=models.CharField(max_length=100),
        ),
    ]