# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20160112_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averagecrossover',
            name='buy_threshold',
            field=models.FloatField(default=0.25),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='first_interval',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='first_type',
            field=models.CharField(default=b'EMA', max_length=3, choices=[(b'TMA', b'TMA'), (b'WMA', b'WMA'), (b'EMA', b'EMA'), (b'SMA', b'SMA')]),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='second_interval',
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='second_type',
            field=models.CharField(default=b'EMA', max_length=3, choices=[(b'TMA', b'TMA'), (b'WMA', b'WMA'), (b'EMA', b'EMA'), (b'SMA', b'SMA')]),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='sell_threshold',
            field=models.FloatField(default=0.25),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='buy_triggers_required',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='sell_triggers_required',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='time_interval',
            field=models.IntegerField(default=3600, choices=[(60, b'1 Minute'), (300, b'5 Minutes'), (900, b'15 Minutes'), (1800, b'30 Minutes'), (3600, b'One Hour')]),
        ),
        migrations.AlterField(
            model_name='tradingbot',
            name='exchange',
            field=models.CharField(default=b'btc-e', max_length=20),
        ),
        migrations.AlterField(
            model_name='tradingbot',
            name='trading_pair',
            field=models.CharField(default=b'btc_usd', max_length=20),
        ),
    ]
