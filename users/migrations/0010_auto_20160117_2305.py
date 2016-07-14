# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20160117_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authkey',
            name='value',
            field=models.CharField(default=b'4fa91258-e339-480a-859d-8789ac31eacd', unique=True, max_length=36),
        ),
    ]
