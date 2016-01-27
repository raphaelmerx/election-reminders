# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 02:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('voters', '0001_initial'),
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('E', 'email'), ('S', 'SMS')], max_length=2)),
                ('sent', models.BooleanField(default=False)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Election')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_before_election', models.DurationField(help_text='Ex: 2 days to send a reminder 2 days before all elections.')),
                ('media_type', models.CharField(choices=[('E', 'email'), ('S', 'SMS')], max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reminders.Schedule'),
        ),
        migrations.AddField(
            model_name='message',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voters.Voter'),
        ),
    ]
