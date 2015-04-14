# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iotshm_dashboard', '0014_auto_20150414_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagnitudeRDS1',
            fields=[
                ('sensor_id', models.CharField(primary_key=True, serialize=False, max_length=300)),
                ('timestamp', models.DateTimeField(primary_key=True)),
                ('magnitude', models.FloatField()),
                ('reading_type', models.IntegerField(primary_key=True)),
                ('healthy', models.IntegerField()),
            ],
            options={
                'db_table': 'Magnitude',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
