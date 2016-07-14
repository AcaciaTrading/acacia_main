# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20160112_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='averagecrossover',
            name='strategy',
        ),
        migrations.AddField(
            model_name='strategy',
            name='average_crossover',
            field=models.OneToOneField(related_name='strategy', null=True, blank=True, to='main.AverageCrossover'),
        ),
    ]
