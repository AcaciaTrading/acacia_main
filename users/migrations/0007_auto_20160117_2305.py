# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160117_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authkey',
            name='value',
            field=models.CharField(default=b'57c34653-fcf9-4fa7-b31b-e62c4e2a6eec', unique=True, max_length=36),
        ),
    ]
