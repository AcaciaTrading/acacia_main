# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20160206_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradingbot',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
    ]
