# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0003_ordertask_trades_made'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertask',
            name='total_trades',
            field=models.IntegerField(default=-1),
        ),
    ]
