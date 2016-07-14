# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20160112_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averagecrossover',
            name='strategy',
            field=models.ForeignKey(related_name='average_crossover', default=1, to='main.Strategy'),
            preserve_default=False,
        ),
    ]
