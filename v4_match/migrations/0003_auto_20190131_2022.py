# Generated by Django 2.1.4 on 2019-01-31 16:52

from django.db import migrations
import django_jalali.db.models
import jdatetime


class Migration(migrations.Migration):

    dependencies = [
        ('v4_match', '0002_auto_20190129_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='multimedia',
            name='upload_time',
            field=django_jalali.db.models.jDateTimeField(default=jdatetime.datetime.now),
        ),
    ]
