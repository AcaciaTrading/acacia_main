# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import time


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_auto_20160216_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_timestamp',
            field=models.IntegerField(default=time.time),
        ),
    ]
