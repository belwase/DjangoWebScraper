# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_crawlerrecord_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawlerrecord',
            name='bytes_downloaded',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerrecord',
            name='end_time',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerrecord',
            name='mailed',
            field=models.NullBooleanField(max_length=25),
        ),
        migrations.AlterField(
            model_name='crawlerrecord',
            name='records_downloaded',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerrecord',
            name='records_merged',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerrecord',
            name='records_new',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='crawlerrecord',
            name='start_time',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
