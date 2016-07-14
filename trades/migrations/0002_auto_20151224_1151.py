# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertask',
            name='start_timestamp',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='ordertask',
            name='amount',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='ordertask',
            name='amount_remaining',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='ordertask',
            name='deadline_timestamp',
            field=models.IntegerField(default=-1),
        ),
    ]
