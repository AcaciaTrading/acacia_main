# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160117_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authkey',
            name='value',
            field=models.CharField(default=b'b5d42f02-24c0-4b03-87ca-ef197bf7ca86', unique=True, max_length=36),
        ),
    ]
