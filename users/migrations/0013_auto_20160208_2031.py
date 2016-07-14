# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20160117_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authkey',
            name='user',
        ),
        migrations.DeleteModel(
            name='AuthKey',
        ),
    ]
