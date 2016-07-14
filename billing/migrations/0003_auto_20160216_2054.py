# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20160216_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='stripe_id',
            field=models.CharField(default=b'', max_length=100, blank=True),
        ),
    ]
