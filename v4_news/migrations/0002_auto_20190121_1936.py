# Generated by Django 2.1.4 on 2019-01-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v4_news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.CharField(max_length=512, null=True),
        ),
    ]