# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_iport_creat_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iport',
            name='creat_time',
        ),
    ]