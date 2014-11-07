# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20141106_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='x_coord',
            field=models.FloatField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='station',
            name='y_coord',
            field=models.FloatField(default=0, null=True),
            preserve_default=True,
        ),
    ]
