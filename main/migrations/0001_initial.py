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
            name='AverageCrossover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_type', models.CharField(max_length=3, choices=[(b'TMA', b'TMA'), (b'WMA', b'WMA'), (b'EMA', b'EMA'), (b'SMA', b'SMA')])),
                ('first_interval', models.IntegerField()),
                ('second_type', models.CharField(max_length=3, choices=[(b'TMA', b'TMA'), (b'WMA', b'WMA'), (b'EMA', b'EMA'), (b'SMA', b'SMA')])),
                ('second_interval', models.IntegerField()),
                ('buy_threshold', models.FloatField()),
                ('sell_threshold', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Backtest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp_start', models.IntegerField()),
                ('teimstamp_end', models.IntegerField()),
                ('profit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BotTrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exchange', models.CharField(max_length=20)),
                ('trading_pair', models.CharField(max_length=20)),
                ('direction', models.CharField(max_length=4)),
                ('amount', models.FloatField()),
                ('timestamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy_threshold', models.FloatField()),
                ('sell_threshold', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('strategy_type', models.IntegerField(choices=[(0, b'Simple rule-based'), (1, b'Complex rule-based'), (2, b'Script-based')])),
                ('time_interval', models.IntegerField(choices=[(60, b'1 Minute'), (300, b'5 Minutes'), (900, b'15 Minutes'), (1800, b'30 Minutes'), (3600, b'One Hour')])),
                ('buy_triggers_required', models.IntegerField()),
                ('sell_triggers_required', models.IntegerField()),
                ('average_crossover', models.OneToOneField(related_name='strategy', to='main.AverageCrossover')),
                ('user', models.ForeignKey(related_name='strategies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TradingBot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exchange', models.CharField(max_length=20)),
                ('trading_pair', models.CharField(max_length=20)),
                ('api_key', models.CharField(max_length=150)),
                ('api_secret', models.CharField(max_length=150)),
                ('api_id', models.CharField(max_length=20)),
                ('strategy', models.ForeignKey(related_name='bots', to='main.Strategy')),
                ('user', models.ForeignKey(related_name='bots', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='indicator',
            name='strategy',
            field=models.ForeignKey(related_name='indicators', to='main.Strategy'),
        ),
        migrations.AddField(
            model_name='bottrade',
            name='bot',
            field=models.ForeignKey(related_name='trades', to='main.TradingBot'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='strategy',
            field=models.ForeignKey(related_name='backtests', to='main.Strategy'),
        ),
    ]
