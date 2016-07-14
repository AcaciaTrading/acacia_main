# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_invoice_paid_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='creation_email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='warning_email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
