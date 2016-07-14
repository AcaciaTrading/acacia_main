# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_tradingbot_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='backtest',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='backtest',
            name='profit',
            field=models.FloatField(default=0.0),
        ),
    ]
