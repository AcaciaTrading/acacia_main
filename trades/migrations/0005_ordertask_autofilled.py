# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0004_ordertask_total_trades'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertask',
            name='autofilled',
            field=models.BooleanField(default=False),
        ),
    ]
