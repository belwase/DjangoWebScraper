# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_facebookpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookpage',
            name='pid',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
