# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20160112_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradingbot',
            name='api_id',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
