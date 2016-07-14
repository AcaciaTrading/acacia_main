# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160112_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='average_crossover',
            field=models.OneToOneField(related_name='strategy', null=True, to='main.AverageCrossover'),
        ),
    ]
