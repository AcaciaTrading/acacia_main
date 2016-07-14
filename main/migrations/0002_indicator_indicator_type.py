# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='indicator_type',
            field=models.CharField(default='ROC', max_length=25, choices=[(b'ROC', b'ROC'), (b'MACD', b'MACD'), (b'RSI', b'RSI')]),
            preserve_default=False,
        ),
    ]
