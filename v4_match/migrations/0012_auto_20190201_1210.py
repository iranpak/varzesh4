# Generated by Django 2.1.4 on 2019-02-01 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v4_player', '0004_merge_20190131_2143'),
        ('v4_match', '0011_auto_20190201_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('گل', 'goal'), ('پاس گل', 'assist'), ('تعویض', 'substitute'), ('کارت قرمز', 'red-card'), ('کارت زرد', 'yellow-card'), ('پرتاب سه امتیازی', '3-points-shot'), ('پرتاب دو امتیازی', 'areal-shot'), ('توپ ربایی', 'steal')], max_length=100)),
                ('is_successful', models.BooleanField(default=True)),
                ('minute', models.IntegerField()),
                ('part_of_game', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='resources/images/event-icons')),
                ('event_type', models.CharField(choices=[('گل', 'goal'), ('پاس گل', 'assist'), ('تعویض', 'substitute'), ('کارت قرمز', 'red-card'), ('کارت زرد', 'yellow-card'), ('پرتاب سه امتیازی', '3-points-shot'), ('پرتاب دو امتیازی', 'areal-shot'), ('توپ ربایی', 'steal')], max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_icon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v4_match.EventIcon'),
        ),
        migrations.AddField(
            model_name='event',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v4_match.Match'),
        ),
        migrations.AddField(
            model_name='event',
            name='player1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_out', to='v4_player.Player'),
        ),
        migrations.AddField(
            model_name='event',
            name='player2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='change_in', to='v4_player.Player'),
        ),
    ]
