# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_strategy_strategy_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradingbot',
            name='primary_reserve',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tradingbot',
            name='secondary_reserve',
            field=models.FloatField(default=0),
        ),
    ]
