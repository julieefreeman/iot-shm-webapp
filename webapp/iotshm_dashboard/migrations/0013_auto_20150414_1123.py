# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0012_healthrds_magnituderds'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='magnituderds',
            table='MagnitudeV2',
        ),
    ]
