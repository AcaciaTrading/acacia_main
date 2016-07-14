# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20160112_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='name',
            field=models.CharField(default=b'Untitled Strategy', max_length=100),
        ),
        migrations.AddField(
            model_name='tradingbot',
            name='name',
            field=models.CharField(default=b'Untitled Bot', max_length=100),
        ),
        migrations.AlterField(
            model_name='tradingbot',
            name='api_key',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='tradingbot',
            name='api_secret',
            field=models.CharField(max_length=150, blank=True),
        ),
    ]
