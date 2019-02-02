# Generated by Django 2.1.4 on 2019-02-02 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v4_player', '0004_merge_20190131_2143'),
        ('v4_team', '0005_merge_20190201_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerFollowings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='v4_player.Player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamFollowings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='v4_team.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='teamfollowings',
            unique_together={('user', 'team')},
        ),
        migrations.AlterUniqueTogether(
            name='playerfollowings',
            unique_together={('user', 'player')},
        ),
    ]
