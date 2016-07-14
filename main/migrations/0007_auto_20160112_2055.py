# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20160112_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategy',
            name='average_crossover',
        ),
        migrations.AddField(
            model_name='averagecrossover',
            name='strategy',
            field=models.OneToOneField(related_name='average_crossover', null=True, blank=True, to='main.Strategy'),
        ),
    ]
