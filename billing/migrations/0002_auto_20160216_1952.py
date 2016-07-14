# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='bitcoin',
        ),
        migrations.AddField(
            model_name='customer',
            name='stripe_id',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
