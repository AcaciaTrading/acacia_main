# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20160208_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='backtest',
            old_name='profit',
            new_name='profit_primary',
        ),
        migrations.AddField(
            model_name='backtest',
            name='profit_secondary',
            field=models.FloatField(default=0.0),
        ),
    ]
