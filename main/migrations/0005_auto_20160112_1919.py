# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160112_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='average_crossover',
            field=models.OneToOneField(related_name='strategy', default='', blank=True, to='main.AverageCrossover'),
            preserve_default=False,
        ),
    ]
