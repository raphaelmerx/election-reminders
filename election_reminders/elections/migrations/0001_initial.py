# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(db_index=True, help_text='When this election will be held.')),
                ('name', models.CharField(help_text='A user friendly name.', max_length=255)),
                ('state', models.CharField(blank=True, help_text='A 2 letter representation of the state. Blank if national election.', max_length=2)),
            ],
        ),
    ]
