# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 02:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_crawlerrecord_keyword'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripAdvisorAttraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('website', models.TextField()),
                ('email', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.TextField()),
                ('keywords', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TripAdvisorCat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('cat', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='TripAdvisorLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('url', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='tripadvisorattraction',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TripAdvisorCat'),
        ),
        migrations.AddField(
            model_name='tripadvisorattraction',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.TripAdvisorLocation'),
        ),
    ]
