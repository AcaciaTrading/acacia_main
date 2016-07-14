# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bitcoin', models.BooleanField(default=False)),
                ('expiry_timestamp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_cents', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(related_name='invoices', to='billing.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_cents', models.IntegerField()),
                ('name', models.CharField(max_length=15)),
                ('num_bots_allowed', models.IntegerField()),
                ('max_trade_size_usd', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='plan',
            field=models.ForeignKey(related_name='subscribers', to='billing.Plan'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
    ]
