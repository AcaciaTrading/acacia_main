# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20160217_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averagecrossover',
            name='first_interval',
            field=models.IntegerField(default=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40)]),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='first_type',
            field=models.CharField(default=b'EMA', max_length=3, choices=[(b'EMA', b'EMA'), (b'DEMA', b'DEMA'), (b'TMA', b'TMA'), (b'TEMA', b'TEMA'), (b'WMA', b'WMA'), (b'SMA', b'SMA')]),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='second_interval',
            field=models.IntegerField(default=21, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40)]),
        ),
        migrations.AlterField(
            model_name='averagecrossover',
            name='second_type',
            field=models.CharField(default=b'EMA', max_length=3, choices=[(b'EMA', b'EMA'), (b'DEMA', b'DEMA'), (b'TMA', b'TMA'), (b'TEMA', b'TEMA'), (b'WMA', b'WMA'), (b'SMA', b'SMA')]),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='indicator_type',
            field=models.CharField(max_length=25, choices=[(b'RSI', b'RSI'), (b'ROC', b'ROC'), (b'MACD', b'MACD'), (b'Stochastic', b'Stochastic'), (b'Aroon Down', b'Aroon Down'), (b'Aroon Up', b'Aroon Up')]),
        ),
    ]
