# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('color', models.IntegerField()),
                ('city', models.ForeignKey(related_name='lines', to='app.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('prev_time', models.IntegerField(null=True, blank=True)),
                ('next_time', models.IntegerField(null=True, blank=True)),
                ('x_coord', models.IntegerField()),
                ('y_coord', models.IntegerField()),
                ('line', models.ForeignKey(related_name='stations', to='app.Line')),
                ('next_station', models.OneToOneField(related_name='prev_station', null=True, blank=True, to='app.Station')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('from_station', models.ForeignKey(related_name='transitions', to='app.Station')),
                ('to_station', models.ForeignKey(to='app.Station')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
