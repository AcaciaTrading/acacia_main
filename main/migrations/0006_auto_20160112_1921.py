# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160112_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='average_crossover',
            field=models.OneToOneField(related_name='strategy', null=True, blank=True, to='main.AverageCrossover'),
        ),
    ]
