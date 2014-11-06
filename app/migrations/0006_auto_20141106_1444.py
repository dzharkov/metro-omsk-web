# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20141106_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='next_station',
            field=models.OneToOneField(related_name='prev_station', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='app.Station'),
            preserve_default=True,
        ),
    ]
