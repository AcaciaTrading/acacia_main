# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authkey',
            name='value',
            field=models.CharField(default=b'4090a4a1-ab08-4f6e-86b9-1a4348dd2e01', unique=True, max_length=36),
        ),
    ]
