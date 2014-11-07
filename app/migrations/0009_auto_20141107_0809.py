# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20141106_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='x_coord',
        ),
        migrations.RemoveField(
            model_name='station',
            name='y_coord',
        ),
        migrations.AddField(
            model_name='city',
            name='bottom_coord',
            field=models.FloatField(default=400),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='left_coord',
            field=models.FloatField(default=-400),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='right_coord',
            field=models.FloatField(default=400),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='top_coord',
            field=models.FloatField(default=-400),
            preserve_default=True,
        ),
    ]
