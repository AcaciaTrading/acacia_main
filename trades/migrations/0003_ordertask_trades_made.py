# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_auto_20151224_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertask',
            name='trades_made',
            field=models.IntegerField(default=0),
        ),
    ]
