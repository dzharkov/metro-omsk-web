# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20141106_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='color',
            field=models.CharField(default=b'#FF0000', max_length=10),
            preserve_default=True,
        ),
    ]
