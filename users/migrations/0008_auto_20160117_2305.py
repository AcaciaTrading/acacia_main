# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160117_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authkey',
            name='value',
            field=models.CharField(default=b'2d7712fb-04f8-4608-aeeb-8a692db63df6', unique=True, max_length=36),
        ),
    ]
