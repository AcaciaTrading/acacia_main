# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20160112_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategy',
            name='strategy_type',
        ),
    ]
