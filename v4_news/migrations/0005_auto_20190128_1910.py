# Generated by Django 2.1.4 on 2019-01-28 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v4_news', '0004_auto_20190121_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(upload_to='resources/images/news'),
        ),
    ]