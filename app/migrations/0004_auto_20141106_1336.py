# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20141106_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='ln_coord',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='lt_coord',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
