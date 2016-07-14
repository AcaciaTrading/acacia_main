# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exchange', models.CharField(max_length=15)),
                ('api_key', models.CharField(max_length=250)),
                ('api_secret', models.CharField(max_length=250)),
                ('api_id', models.CharField(max_length=50, blank=True)),
                ('trading_pair', models.CharField(max_length=10)),
                ('direction', models.CharField(max_length=4)),
                ('amount', models.FloatField()),
                ('amount_remaining', models.FloatField()),
                ('deadline_timestamp', models.IntegerField()),
                ('user', models.ForeignKey(related_name='order_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
