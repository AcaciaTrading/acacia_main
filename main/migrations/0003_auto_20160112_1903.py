# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_indicator_indicator_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='backtest',
            old_name='teimstamp_end',
            new_name='timestamp_end',
        ),
        migrations.AddField(
            model_name='backtest',
            name='exchange',
            field=models.CharField(default='btc-e', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='backtest',
            name='trading_pair',
            field=models.CharField(default='btc_usd', max_length=20),
            preserve_default=False,
        ),
    ]
