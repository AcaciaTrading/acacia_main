# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20160302_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='paid_timestamp',
            field=models.IntegerField(default=0),
        ),
    ]
