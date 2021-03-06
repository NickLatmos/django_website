# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-11 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.IntegerField()),
                ('humidity', models.IntegerField()),
                ('case_temperature', models.IntegerField()),
                ('pressure', models.IntegerField()),
                ('weather', models.CharField(max_length=30)),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('weather_station_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('owner_name', models.CharField(max_length=40)),
                ('owner_surname', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Valve',
            fields=[
                ('ID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='weather_station.WeatherStation')),
                ('valve_status', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='weather',
            name='ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather_station.WeatherStation'),
        ),
    ]
